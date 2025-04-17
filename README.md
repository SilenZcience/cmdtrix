<div id="top"></div>

<p>
   <a href="https://pepy.tech/project/cmdtrix/" alt="Downloads">
      <img src="https://static.pepy.tech/personalized-badge/cmdtrix?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads" align="right">
   </a>
   <a href="https://pypi.org/project/cmdtrix/" alt="Visitors">
      <img src="https://hitscounter.dev/api/hit?url=https%3A%2F%2Fgithub.com%2FSilenZcience%2Fcmdtrix&label=Visitors&icon=person-circle&color=%23479f76" align="right">
   </a>
   <a href="https://github.com/SilenZcience/cmdtrix/tree/main/cmdtrix/" alt="CodeSize">
      <img src="https://img.shields.io/github/languages/code-size/SilenZcience/cmdtrix?color=purple" align="right">
   </a>
</p>

[![OS-Windows]][OS-Windows]
[![OS-Linux]][OS-Linux]
[![OS-MacOS]][OS-MacOS]

<br/>
<div align="center">
<h2 align="center">cmdtrix</h2>
   <p align="center">
      matrix-console-effect made in Python.
      <br/>
      <a href="https://github.com/SilenZcience/cmdtrix/blob/main/cmdtrix/main.py">
         <strong>Explore the code »</strong>
      </a>
      <br/>
      <br/>
      <a href="https://github.com/SilenZcience/cmdtrix/issues">Report Bug</a>
      ·
      <a href="https://github.com/SilenZcience/cmdtrix/issues">Request Feature</a>
   </p>
</div>


<details>
   <summary>Table of Contents</summary>
   <ol>
      <li>
         <a href="#about-the-project">About The Project</a>
         <ul>
            <li><a href="#made-with">Made With</a></li>
         </ul>
      </li>
      <li>
         <a href="#getting-started">Getting Started</a>
         <ul>
            <li><a href="#prerequisites">Prerequisites</a></li>
            <li><a href="#installation">Installation</a></li>
         </ul>
      </li>
      <li><a href="#usage">Usage</a>
         <ul>
         <li><a href="#examples">Examples</a></li>
         </ul>
      </li>
      <li><a href="#license">License</a></li>
      <li><a href="#contact">Contact</a></li>
   </ol>
</details>

<div id="about-the-project"></div>

## About The Project

This project simply emulates "The Matrix"-effect on any console-terminal.

<div id="made-with"></div>

### Made With
[![Python][MadeWith-Python]](https://www.python.org/)
[![Python][Python-Version]](https://www.python.org/)

<p align="right">(<a href="#top">back to top</a>)</p>
<div id="getting-started"></div>

## Getting Started

<div id="prerequisites"></div>

### Prerequisites

It is necessary that a font is installed that supports the unicode characters used (greek, cyrillic).

<div id="installation"></div>

### Installation
[![Version][CurrentVersion]](https://pypi.org/project/cmdtrix/)

1. install the python package ([PyPI-cmdtrix](https://pypi.org/project/cmdtrix/)):
```console
pip install cmdtrix
```
```console
pip install git+https://github.com/SilenZcience/cmdtrix.git
```
<p align="right">(<a href="#top">back to top</a>)</p>
<div id="usage"></div>

## Usage

```console
cmdtrix [-h] [-c COLOR] ...
```
```console
python -m cmdtrix [-h] [-c COLOR] ...
```

| Argument               | Description                                                          |
|------------------------|----------------------------------------------------------------------|
| -h, --help             | show help message and exit                                           |
| -v, --version          | output version information                                           |
| -s, --synchronous      | sync the matrix columns speed                                        |
| -c [\*], --color [\*]  | set the main-color to *                                              |
| -p [\*], --peak [\*]   | set the peak-color to *                                              |
| -d p, --dim p          | add chance p (percent) for dim characters                            |
| -i p, --italic p       | add chance p (percent) for italic characters                         |
| -m * p c               | hide a custom message * within the Matrix, with chance p and color c |
| -S \*, --symbols \*    | set a custom series of symbols to choose from                        |
| -j, --japanese         | use japanese characters (overrides -S; requires appropriate fonts)   |
| --framedelay DELAY     | set the framedelay (in sec) to slow down the Matrix, default is 0.015|
| --timer DELAY          | exit the Matrix after DELAY (in sec) automatically                   |
| --onkey                | only spawn columns on key-press                                      |

<div id="examples"></div>

### Examples

```console
cmdtrix -m SilenZcience 5 red -m cmdtrix 5 blue -d 5 -m Star*The*Repo 10 magenta
```
> ![Example0](https://raw.githubusercontent.com/SilenZcience/cmdtrix/main/img/cmdtrix.gif "example0")

<!-- ![Example1](https://raw.githubusercontent.com/SilenZcience/cmdtrix/main/img/example1.gif "example1") -->

![Example2](https://raw.githubusercontent.com/SilenZcience/cmdtrix/main/img/example2.gif "example2")

![Example2](https://raw.githubusercontent.com/SilenZcience/cmdtrix/main/img/example3.gif "example3")

<p align="right">(<a href="#top">back to top</a>)</p>
<div id="license"></div>

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/SilenZcience/cmdtrix/blob/main/LICENSE) file for details

<div id="contact"></div>

## Contact

> **SilenZcience** <br/>
[![GitHub-SilenZcience][GitHub-SilenZcience]](https://github.com/SilenZcience)

[OS-Windows]: https://img.shields.io/badge/os-windows-green
[OS-Linux]: https://img.shields.io/badge/os-linux-green
[OS-MacOS]: https://img.shields.io/badge/os-macOS-green

[MadeWith-Python]: https://img.shields.io/badge/Made%20with-Python-brightgreen
[Python-Version]: https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue

[CurrentVersion]: https://img.shields.io/pypi/v/cmdtrix.svg

[GitHub-SilenZcience]: https://img.shields.io/badge/GitHub-SilenZcience-orange
