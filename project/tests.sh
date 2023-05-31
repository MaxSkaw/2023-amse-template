echo === Start Pipeline ===
python ../data/pipeline.py
echo === Begin testing ===

echo === Checking for databases ===
python test.py

echo === Testing finished ===