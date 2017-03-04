# YTRSS - Youtube subscription downloader

Program do pobierania listy adresów url na podstawie adresów subskrypcji lub wybranych playlist.

![Author](https://img.shields.io/badge/author-Rafa%C5%82%20Kobel-blue.svg)
![BitbucketIssues](https://img.shields.io/bitbucket/issues/rafyco/ytrss.svg)
![version](https://img.shields.io/pypi/v/ytrss.svg)
![License](https://img.shields.io/badge/license-GNU-blue.svg)

## instalacja

### PyPi

    sudo pip install ytrss

### setup.py

    sudo python setup.py install

## Wywołanie

    ytrss_subs --help

## Przykładowy plik kofiguracyjny

    vi ~/.conf/ytrss/config


```
{
    "output"   : "<output_file>",
    "subscriptions" : [
        {
            "code"    : "<playlist_id>",
            "type"    : "playlist"
        },
        {
            "code"    : "<subscritpion_id>"
        },
        {
            "code"    : "<subscription_id>", 
            "enabled" : false
        }
    ]            
}

```

## Autor

Rafał Kobel <rafalkobel@rafyco.pl>

## Licencja

>    Copyright (C) 2017  Rafal Kobel <rafalkobel@rafyco>
>
>    This program is free software: you can redistribute it and/or modify
>    it under the terms of the GNU General Public License as published by
>    the Free Software Foundation, either version 3 of the License, or
>    (at your option) any later version.
>
>    This program is distributed in the hope that it will be useful,
>    but WITHOUT ANY WARRANTY; without even the implied warranty of
>    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
>    GNU General Public License for more details.
>
>    You should have received a copy of the GNU General Public License
>    along with this program.  If not, see <http://www.gnu.org/licenses/>.

