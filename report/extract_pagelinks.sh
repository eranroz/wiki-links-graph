
# get latest dumps
dump=20160305
wiki=enwiki
wget http://dumps.wikimedia.org/$wiki/$dump/$wiki-$dump-page.sql.gz
wget http://dumps.wikimedia.org/$wiki/$dump/$wiki-$dump-pagelinks.sql.gz
wget http://dumps.wikimedia.org/$wiki/$dump/$wiki-$dump-page_props.sql.gz

zcat $wiki-$dump-page.sql.gz | python ../mysqldump-to-csv/mysqldump_to_csv.py | awk -F , '{if ($2==0){print $0}}' | gzip > $wiki-$dump-page.csv.gz
zcat $wiki-$dump-pagelinks.sql.gz | python ../mysqldump-to-csv/mysqldump_to_csv.py | awk -F , '{if ($2==0){print $0}}' | gzip > $wiki-$dump-pagelinks.csv.gz
zcat $wiki-$dump-page_props.sql.gz | python ../mysqldump-to-csv/mysqldump_to_csv.py | awk -F , '{if ($2 ~ /^disambiguation$/){print $1}}' > disambig_ids_$wiki
