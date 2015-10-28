# prepare data
#python prepare-data.py 2015-09-01 2015-09-30 5 ../output/train-data
#python prepare-data.py 2015-08-01 2015-08-31 5 ../output/test-data

# Build model
#svm-scale -s ./model/train-data-scale-info ../output/train-data > ../output/train-data.scale
#svm-train -b 1 ../output/train-data.scale ./model/train-model

# Test model
#svm-scale -r train-data-scale-info test-data > test-data.scale
#svm-predict -b 1 test-data.scale model/train-model test-result

# Generate the predicting data
#python ./generate-predict-data.py $1 5 ../output/predict-data ../output/predict-stock-list

# Predict
#svm-scale -r model/train-data-scale-info ../output/predict-data > ../output/predict-data.scale
#svm-predict -b 1 ../output/predict-data.scale model/train-model ../output/predict-result

# Make decision
python ./make-decision.py ../output/predict-result ../output/predict-stock-list ../commit/$1.json

