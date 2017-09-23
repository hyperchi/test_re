```
# -h see helps
python3 main.py -h

# -i specific an single id or id_file path(with every id as a line.)
python3 main.py -i 167385960
python3 main.py -i ./id_file

# -f specific filter mode, if 0, all weibo are all original, if 1, contains repost one, default is 0
python3 main.py -i 16758795 -f 0

# -d specific debug mode for testing, be aware debug mode only support one single id.
python3 main.py -i 178600077 -d 1
```

