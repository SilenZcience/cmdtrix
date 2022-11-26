<div id="top"></div>

<p>
   <a href="https://pypi.org/project/cmdtrix/" alt="Downloads">
      <img src="https://static.pepy.tech/personalized-badge/cmdtrix?period=total&units=international_system&left_color=grey&right_color=orange&left_text=Downloads" align="right">
   </a>
   <a href="https://pypi.org/project/cmdtrix/" alt="Visitors">
      <img src="https://visitor-badge.laobi.icu/badge?page_id=SilenZcience.cmdtrix" align="right">
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

## About The Project

This project simply emulates "The Matrix"-effect on any console-terminal.

### Made With
[![Python][MadeWith-Python]](https://www.python.org/)

<p align="right">(<a href="#top">back to top</a>)</p>

## Getting Started

### Prerequisites

It is neccessary that a font is installed, which supports the unicode characters used (greek, cyrillic).

### Installation

1. install the python package ([PyPI-cmdtrix](https://pypi.org/project/cmdtrix/)):
```console
pip install cmdtrix
```
or
```console
pip install git+https://github.com/SilenZcience/cmdtrix.git
```
<p align="right">(<a href="#top">back to top</a>)</p>

## Usage

```console
cmdtrix [-h] [-c COLOR] ...
```

| Argument               | Description                                        |
|------------------------|----------------------------------------------------|
| -v, --version          | number all output lines                            |
| -s, --synchronous      | sync the matrix columns speed                      |
| -c [\*], --color [\*]  | set the color to *                                 |
| -d x%, --dim x%        | add chance for dim characters                      |
| -i x%, --italic x%     | add chance for italic characters                   |
| -m * x%                | hide a custom message within the Matrix            |
| --framedelay DELAY     | set the framedelay (in sec) to slow down the Matrix|
| --timer DELAY          | exit the Matrix after DELAY (in sec) automatically |

### Examples

![Example1](https://raw.githubusercontent.com/SilenZcience/cmdtrix/main/img/example1.png "example1")

![Example2](https://raw.githubusercontent.com/SilenZcience/cmdtrix/main/img/example2.png "example2")

<p align="right">(<a href="#top">back to top</a>)</p>

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/SilenZcience/cmdtrix/blob/main/LICENSE) file for details

## Contact

> **SilenZcience** <br/>
[![GitHub-SilenZcience][GitHub-SilenZcience]](https://github.com/SilenZcience)

[OS-Windows]: https://svgshare.com/i/ZhY.svg
[OS-Linux]: https://svgshare.com/i/Zhy.svg
[OS-MacOS]: https://svgshare.com/i/ZjP.svg

[MadeWith-Python]: https://img.shields.io/badge/Made%20with-Python-brightgreen

[GitHub-SilenZcience]: https://img.shields.io/badge/GitHub-SilenZcience-orange