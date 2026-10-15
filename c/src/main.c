#define _POSIX_C_SOURCE 200809L

#include <stdio.h>
#include <signal.h>
#include <wchar.h>
#include <locale.h>
#include <stdlib.h>
#include <stdbool.h>
#include <sys/ioctl.h>
#include <time.h>
#include <string.h>
#include <unistd.h>
#include <ctype.h>
#include <math.h>

#include "chars.h"
#include "arraylist.h"
#include "cascade.h"
#include "delay.h"
#include "color.h"
#include "message.h"

struct winsize w;
bool running = true;

#define MAX_BUF 4096000
char frame_buffer[MAX_BUF];
size_t frame_buf_pos = 0;

/* python defaults: 1% dim, 1% italic */
double chance_for_dim = 0.01;
double chance_for_italic = 0.01;
double chance_for_bottom_up = 0.0;
double frame_delay = 0.015;
Color color_main = {32, 0, 0, 0, false};
Color color_peak = {37, 0, 0, 0, false};

Message messages[MAX_MESSAGES];
int message_count = 0;
Message user_messages[MAX_MESSAGES];
int user_message_count = 0;

bool rainbow = false;
double rainbow_hue = 0.25;

bool timer_enabled = false;
double timer_delay = 0.0;

static const char* const COLOR_CHOICES[] = {
    "black", "red", "green", "yellow", "blue",
    "magenta", "cyan", "white", "orange", "pink",
};
#define COLOR_CHOICES_COUNT ((int)(sizeof(COLOR_CHOICES) / sizeof(COLOR_CHOICES[0])))

void sigint_handler(int signum) {
    (void)signum;
    running = false;
}

void init(void) {
    fprintf(stdout, "\x1b[?1049h\x1b[?25l\x1b[2J");
    fflush(stdout);
}

void deinit(void) {
    fprintf(stdout, "\x1b[m\x1b[2J\x1b[?25h\x1b[?1049l");
    fflush(stdout);
}

void buffer_append(const char* s) {
    size_t len = strlen(s);
    if (frame_buf_pos + len < MAX_BUF) {
        memcpy(frame_buffer + frame_buf_pos, s, len);
        frame_buf_pos += len;
    }
}

static void hsv_to_rgb_unit(double h, int* r, int* g, int* b) {
    h = h - floor(h);
    double i = h * 6.0;
    int ii = (int)i % 6;
    double f = i - ii;
    if (ii == 0) { *r = 255; *g = (int)(255*f); *b = 0; return; }
    if (ii == 1) { *r = 255 - (int)(255*f); *g = 255; *b = 0; return; }
    if (ii == 2) { *r = 0; *g = 255; *b = (int)(255*f); return; }
    if (ii == 3) { *r = 0; *g = 255 - (int)(255*f); *b = 255; return; }
    if (ii == 4) { *r = (int)(255*f); *g = 0; *b = 255; return; }
    *r = 255; *g = 0; *b = 255 - (int)(255*f);
}

/* python's random() always yields [0.0, 1.0) */
static double random_unit(void) {
    return (double)rand() / ((double)RAND_MAX + 1.0);
}

/* renders one frame-buffer cell exactly like python's flushFrameBuffer():
   cursor position first, then the style + color code, then the character */
void print_at(wchar_t s, int x, int y, Color color, const char* style) {
    char tmp[1024];
    const char* st = (style && style[0] != '\0') ? style : "0;";
    if (color.use_rgb) {
        snprintf(tmp, sizeof(tmp), "\x1b[%d;%df\x1b[%s38;2;%d;%d;%dm", y, x, st, color.r, color.g, color.b);
    } else {
        snprintf(tmp, sizeof(tmp), "\x1b[%d;%df\x1b[%s%dm", y, x, st, color.ansi);
    }
    buffer_append(tmp);
    char utf8[MB_CUR_MAX + 1];
    mbstate_t state;
    memset(&state, 0, sizeof(state));
    size_t n = wcrtomb(utf8, s, &state);
    if (n != (size_t)-1) {
        utf8[n] = '\0';
        buffer_append(utf8);
    }
}

void flush_buffer(void) {
    if (frame_buf_pos > 0) {
        fwrite(frame_buffer, 1, frame_buf_pos, stdout);
        fflush(stdout);
        frame_buf_pos = 0;
    }
}

static void add_cascade(ArrayList* al, bool bottom_up) {
    int col = rand() % (w.ws_col + 1);
    al_append(al, cascade_init(col, w.ws_row, bottom_up));
}

void update_cascades(ArrayList* al, Chars* chars) {
    if (rainbow) {
        rainbow_hue = fmod(rainbow_hue + 0.0001, 1.0);
        int r, g, b;
        /* python: COLOR = hsv_to_rgb_unit(RAINBOW_HUE) */
        hsv_to_rgb_unit(rainbow_hue, &r, &g, &b);
        color_main.ansi = 0;
        color_main.r = r;
        color_main.g = g;
        color_main.b = b;
        color_main.use_rgb = true;
        /* python: COLOR_PEAK = hsv_to_rgb_unit(1.0 - RAINBOW_HUE) - inverted! */
        hsv_to_rgb_unit(1.0 - rainbow_hue, &r, &g, &b);
        color_peak.ansi = 0;
        color_peak.r = r;
        color_peak.g = g;
        color_peak.b = b;
        color_peak.use_rgb = true;
    }
    for (int i = 0; i < al->size; i++) {
        wchar_t ch = (wchar_t)chars->chars[rand() % chars->length];
        cascade_update(al->arr[i], w.ws_row, ch, print_at);
        if (al->arr[i]->finished) {
            /* a finished cascade keeps its direction (python's reset() keeps the class) */
            int col = rand() % (w.ws_col + 1);
            cascade_reset(al->arr[i], col, w.ws_row, al->arr[i]->bottom_up);
        }
    }
    /* python adds exactly one new column per tick until the width is reached */
    if (al->size < w.ws_col) {
        bool bottom_up = random_unit() < chance_for_bottom_up;
        add_cascade(al, bottom_up);
    }
}

/* python checks the terminal size every 8 seconds (EventTimer) */
static void check_terminal_size(void) {
    struct winsize nw;
    if (ioctl(0, TIOCGWINSZ, &nw) < 0 || nw.ws_row <= 0 || nw.ws_col <= 0) {
        return;
    }
    if (nw.ws_row != w.ws_row || nw.ws_col != w.ws_col) {
        w = nw;
        fprintf(stdout, "\x1b[2J");
        fflush(stdout);
    }
}

static double now_seconds(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1000000000.0;
}

static bool is_valid_color(const char* name) {
    for (int i = 0; i < COLOR_CHOICES_COUNT; i++) {
        if (strcmp(name, COLOR_CHOICES[i]) == 0) {
            return true;
        }
    }
    return false;
}

static Color color_from_name(const char* name) {
    Color c = {32, 0, 0, 0, false};
    if (strcmp(name, "black") == 0) c.ansi = 30;
    else if (strcmp(name, "red") == 0) c.ansi = 31;
    else if (strcmp(name, "green") == 0) c.ansi = 32;
    else if (strcmp(name, "yellow") == 0) c.ansi = 33;
    else if (strcmp(name, "blue") == 0) c.ansi = 34;
    else if (strcmp(name, "magenta") == 0) c.ansi = 35;
    else if (strcmp(name, "cyan") == 0) c.ansi = 36;
    else if (strcmp(name, "white") == 0) c.ansi = 37;
    else if (strcmp(name, "orange") == 0) { c.r = 255; c.g = 165; c.b = 0; c.use_rgb = true; }
    else if (strcmp(name, "pink") == 0) { c.r = 255; c.g = 71; c.b = 156; c.use_rgb = true; }
    return c;
}

static void print_help(void) {
    printf("Usage: cmdtrix [options]\n\n");
    printf("Options:\n");
    printf("  -c, --color [*]     set the main-color to *\n");
    printf("  -p, --peak [*]      set the peak-color to *\n");
    printf("  -d, --dim p         add chance p (%%) for dim characters\n");
    printf("  -i, --italic p      add chance p (%%) for italic characters\n");
    printf("  -b, --bottomup p    add chance p (%%) for bottom-up cascades\n");
    printf("  -r, --rainbow       enable rainbow color transitions\n");
    printf("  -m * p c            hide a custom message * within the Matrix, with chance p and color c\n");
    printf("  -S, --symbols *     set a custom series of symbols\n");
    printf("  -j, --japanese      use japanese characters\n");
    printf("  --framedelay DELAY  set the framedelay (in sec), default is 0.015\n");
    printf("  --timer DELAY       exit the Matrix after DELAY (in sec) automatically\n");
    printf("  -h, --help          show help\n");
    printf("  -v, --version       show version\n");
    exit(0);
}

static void parse_args(int argc, char** argv, wchar_t** extra_chars, int* extra_len, bool* use_japanese, double* framedelay_out) {
    *use_japanese = false;
    *extra_len = 0;
    *extra_chars = NULL;
    *framedelay_out = frame_delay;
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-h") == 0 || strcmp(argv[i], "--help") == 0) {
            print_help();
        } else if (strcmp(argv[i], "-v") == 0 || strcmp(argv[i], "--version") == 0) {
            printf("cmdtrix 0.2.3\n");
            exit(0);
        } else if (strcmp(argv[i], "-j") == 0 || strcmp(argv[i], "--japanese") == 0) {
            *use_japanese = true;
        } else if ((strcmp(argv[i], "-d") == 0 || strcmp(argv[i], "--dim") == 0) && i + 1 < argc) {
            chance_for_dim = atof(argv[++i]) / 100.0;
            if (chance_for_dim < 0) chance_for_dim = 0;
            if (chance_for_dim > 1) chance_for_dim = 1;
        } else if ((strcmp(argv[i], "-i") == 0 || strcmp(argv[i], "--italic") == 0) && i + 1 < argc) {
            chance_for_italic = atof(argv[++i]) / 100.0;
            if (chance_for_italic < 0) chance_for_italic = 0;
            if (chance_for_italic > 1) chance_for_italic = 1;
        } else if ((strcmp(argv[i], "-b") == 0 || strcmp(argv[i], "--bottomup") == 0) && i + 1 < argc) {
            chance_for_bottom_up = atof(argv[++i]) / 100.0;
            if (chance_for_bottom_up < 0) chance_for_bottom_up = 0;
            if (chance_for_bottom_up > 1) chance_for_bottom_up = 1;
        } else if ((strcmp(argv[i], "-c") == 0 || strcmp(argv[i], "--color") == 0) && i + 1 < argc) {
            const char* cname = argv[++i];
            if (!is_valid_color(cname)) {
                fprintf(stderr, "cmdtrix: error: argument -c/--color: invalid choice: '%s' (choose from black, red, green, yellow, blue, magenta, cyan, white, orange, pink)\n", cname);
                exit(2);
            }
            color_main = color_from_name(cname);
        } else if ((strcmp(argv[i], "-p") == 0 || strcmp(argv[i], "--peak") == 0) && i + 1 < argc) {
            const char* cname = argv[++i];
            if (!is_valid_color(cname)) {
                fprintf(stderr, "cmdtrix: error: argument -p/--peak: invalid choice: '%s' (choose from black, red, green, yellow, blue, magenta, cyan, white, orange, pink)\n", cname);
                exit(2);
            }
            color_peak = color_from_name(cname);
        } else if (strcmp(argv[i], "-r") == 0 || strcmp(argv[i], "--rainbow") == 0) {
            rainbow = true;
        } else if (strcmp(argv[i], "-m") == 0 && i + 1 < argc) {
            if (user_message_count < MAX_MESSAGES) {
                char* msgstr = argv[++i];
                double mchance = 0.01; /* python's default for user messages */
                int mcol = -1;         /* -1 = no explicit color -> follows the main color */
                int mr = 0, mg = 0, mb = 0;
                bool muse_rgb = false;

                /* optional chance in percent */
                if (i + 1 < argc) {
                    char* end = NULL;
                    double v = strtod(argv[i + 1], &end);
                    if (end != argv[i + 1] && end != NULL && *end == '\0') {
                        mchance = v / 100.0;
                        if (mchance < 0) mchance = 0;
                        if (mchance > 1) mchance = 1;
                        i++;
                    }
                }
                /* optional color, only consumed when it is a known color name */
                if (i + 1 < argc && is_valid_color(argv[i + 1])) {
                    Color c = color_from_name(argv[++i]);
                    mcol = c.ansi;
                    mr = c.r;
                    mg = c.g;
                    mb = c.b;
                    muse_rgb = c.use_rgb;
                }
                int mlen = (int)mbstowcs(NULL, msgstr, 0);
                if (mlen >= 0) {
                    Message* me = &user_messages[user_message_count++];
                    me->text = malloc((mlen + 1) * sizeof(wchar_t));
                    mbstowcs(me->text, msgstr, mlen + 1);
                    me->len = mlen;
                    me->chance = mchance;
                    me->color_ansi = mcol;
                    me->r = mr;
                    me->g = mg;
                    me->b = mb;
                    me->use_rgb = muse_rgb;
                }
            }
        } else if (strcmp(argv[i], "--framedelay") == 0 && i + 1 < argc) {
            *framedelay_out = atof(argv[++i]);
            if (*framedelay_out < 0.0) {
                printf("A negative framedelay cannot be implemented!\n");
                exit(1);
            }
        } else if (strcmp(argv[i], "--timer") == 0 && i + 1 < argc) {
            timer_delay = atof(argv[++i]);
            timer_enabled = true;
        } else if ((strcmp(argv[i], "-S") == 0 || strcmp(argv[i], "--symbols") == 0) && i + 1 < argc) {
            const char* sym = argv[++i];
            size_t n = mbstowcs(NULL, sym, 0);
            if (n != (size_t)-1) {
                free(*extra_chars);
                *extra_chars = NULL;
                *extra_len = 0;
                if (n > 0) {
                    wchar_t* wbuf = malloc((n + 1) * sizeof(wchar_t));
                    if (wbuf && mbstowcs(wbuf, sym, n + 1) != (size_t)-1) {
                        *extra_chars = wbuf;
                        *extra_len = (int)n;
                    } else {
                        free(wbuf);
                    }
                }
            }
        }
    }
}

int main(int argc, char** argv) {
    signal(SIGINT, sigint_handler);
    setlocale(LC_ALL, "");
    if (ioctl(0, TIOCGWINSZ, &w) < 0 || w.ws_row <= 0 || w.ws_col <= 0) {
        w.ws_row = 24;
        w.ws_col = 80;
    }
    srand((unsigned)time(NULL));
    wchar_t* extra_chars = NULL;
    int extra_len = 0;
    bool use_japanese = false;
    double framedelay_out = frame_delay;
    parse_args(argc, argv, &extra_chars, &extra_len, &use_japanese, &framedelay_out);
    {
        /* python's HIDDEN_MESSAGE: the default message comes first, then the user messages */
        const char* defmsg = "MadeBySilasKraume";
        int mlen = (int)mbstowcs(NULL, defmsg, 0);
        if (mlen >= 0 && message_count < MAX_MESSAGES) {
            Message* me = &messages[message_count++];
            me->text = malloc((mlen + 1) * sizeof(wchar_t));
            mbstowcs(me->text, defmsg, mlen + 1);
            me->len = mlen;
            me->chance = 0.0005;
            me->color_ansi = -1; /* no explicit color -> follows the main color */
            me->use_rgb = false;
            me->r = me->g = me->b = 0;
        }
        for (int i = 0; i < user_message_count && message_count < MAX_MESSAGES; i++) {
            messages[message_count++] = user_messages[i];
        }
    }
    Chars* chars = chars_init(extra_chars, extra_len, use_japanese);
    if (extra_chars) free(extra_chars);
    ArrayList al;
    al_init(&al);
    init();
    double start_time = now_seconds();
    double last_size_check = start_time;
    while (running) {
        update_cascades(&al, chars);
        flush_buffer();
        double now = now_seconds();
        if (timer_enabled && now - start_time >= timer_delay) {
            break;
        }
        if (now - last_size_check >= 8.0) {
            last_size_check = now;
            check_terminal_size();
        }
        dsleep(framedelay_out);
    }
    deinit();
    for (int i = 0; i < al.size; i++) {
        cascade_destroy(al.arr[i]);
    }
    al_destroy(&al);
    chars_destroy(chars);
    return 0;
}
