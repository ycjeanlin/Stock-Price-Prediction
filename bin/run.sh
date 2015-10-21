# prepare data
python prepare-data.py 2015-07-01 2015-07-31 5 ../ex3/train-data
python prepare-data.py 2015-08-01 2015-08-31 5 ../ex3/test-data

# Build model
cd ../ex3
svm-scale -s train-data-scale-info train-data > train-data.scale
svm-train -b 1 train-data.scale model/train-model

# Test model
svm-scale -r train-data-scale-info test-data > test-data.scale
svm-predict -b 1 test-data.scale model/train-model test-result

