# Generate the predicting data
python ./generate-predict-data.py $1 5 ../output/predict-data ../output/predict-stock-list

# Predict
svm-scale -r model/train-data-scale-info ../output/predict-data > ../output/predict-data.scale
svm-predict -b 1 ../output/predict-data.scale model/train-model ../output/predict-result

# Make decision
python ./make-decision.py ../output/predict-result ../output/predict-stock-list ../commit/$1.json

