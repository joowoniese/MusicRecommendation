# MusicRecommendationModel
### Recommendation of music similiar music with music that user select 


![Architecture](https://github.com/joowoniese/MusicRecommendation/blob/main/ModelInfo/Musicdata.png)
![Architecture](https://github.com/joowoniese/MusicRecommendation/blob/main/ModelInfo/MusicRecommendation_logics.png)

## Virtual Environment Setup
Conda
```
# clone project
git clone https://github.com/joowoniese/MusicRecommendation.git
cd MusicRecommendation

# create conda environment
conda create -n MuiscRecommendation python==3.9
conda activate MuiscRecommendation

# install packages/librarys
pip install -r requirements.txt
```

## Run Music Recommendation
Python
```
python musicRecommendation.py

# Input song name in json file
# Three similiar song with your song selected will be out
```
