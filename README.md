#ytrss

Program do pobierania listy adresów url na podstawie adresów subskrypcji lub wybranych playlist.		

## Wywołanie

	python -m ytrss.subs --help	

## Przykładowy plik kofiguracyjny

    vi ~/.subs_conf


```
{
    "database" : "<database_file>",
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

