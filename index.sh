python src/indexer.py $1 $2

mv $2/index0 $2/initialIndex
python src/secondIndex.py $2/initialIndex $2/secondIndex
python src/synonymIndex.py $2/secondIndex $2/synonymIndex
python src/titlesIndex.py $1 $2/titlesIndex

python src/searcher.py $2