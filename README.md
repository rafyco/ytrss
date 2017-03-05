# YTRSS - Youtube subscription downloader

Program to automatic download YouTube files by youtube_dl scripts.

![Author](https://img.shields.io/badge/author-Rafa%C5%82%20Kobel-blue.svg)
![BitbucketIssues](https://img.shields.io/bitbucket/issues/rafyco/ytrss.svg)
![version](https://img.shields.io/pypi/v/ytrss.svg)
![License](https://img.shields.io/badge/license-GNU-blue.svg)

## Instalation

### PyPi

    sudo pip install ytrss

### setup.py

    sudo python setup.py install

## Usage

Download information about new subscription.

    ytrss_subs
    
Download files from queue.
    
    ytrss_daemon
    
Add new file to queue
    
    ytdown <file_url>

## Example configuration

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

## Author

Rafal Kobel <rafalkobel@rafyco.pl>

## License

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

