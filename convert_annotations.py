import pandas as pd
import os

annotation_location = 'Annotations/piezo_annot_v4.csv'

# Creates Audacity annotation file for each clip
def convert_annotations_individual(annotation):
    target_directory = './Annotations/' 

    # Read and clean DataFrame
    df = pd.read_csv(annotation)
    df['onset_s'] = df['onset_s'].round(decimals = 6) 
    df['offset_s'] = df['offset_s'].round(decimals = 6)
    groups = df.groupby('audio_path')

    # Will create converted .txt file for each file listed in annotations
    for item in groups.groups:
        path = target_directory + '/' + item + '.txt'
        if os.path.exists(path):
            os.remove(path)
        temp = groups.get_group(item).drop(df.iloc[:, 3:],axis = 1)
        #print(temp.head(5))
        temp = temp[['onset_s','offset_s','label']]
        temp_song = temp.loc[temp['label'].isin(['g','h','i','j'])] # List of syllables we want, drop all other rows
        temp_song['label'] = temp_song['label'].replace({'g':'a', 'h':'b', 'i':'c', 'j':'d'})
        #temp_song.rename(columns={'g':'a', 'h':'b', 'i':'c', 'j':'d'})

        
        temp_song.to_csv(path, header=False, index=False,sep ='\t')

# Creates Audacity annotation file relative to entire dataframe
def convert_annotations_master(annotation):
    path = './Annotations/annotations_master.txt';
    df = pd.read_csv(annotation);
    #df['onset_s'] = df['onset_s'].round(decimals = 6);
    #df['offset_s'] = df['offset_s'].round(decimals = 6);
    fs = 30_000; # Our sampling rate
    
    grouped = df.groupby('audio_path');
    
    #df_converted = pd.DataFrame()
    df_temp = [];
    for item in grouped.groups:
        temp = grouped.get_group(item).drop(df.iloc[:, 3:],axis = 1);
        
        # Gets annotation location relative to original audio.
        temp_split = item.split('.')[0].split('_')
        segment_index = int(temp_split[3]);
        sample_index = int(temp_split[4]);
        relative_location = (segment_index + sample_index) / fs;
        
        # Convert onset and offset to relative.
        temp['onset_s'] = temp['onset_s'] + relative_location;
        temp['offset_s'] = temp['offset_s'] + relative_location;
        df_temp.append(temp);
    
    # Created converted dataframe
    df_converted = pd.concat(df_temp);
    df_converted = df_converted[['onset_s','offset_s','label']];
    df_converted = df_converted.loc[df_converted['label'].isin(['g','h','i','j'])]; # List of syllables we want, drop all other rows
    df_converted['label'] = df_converted['label'].replace({'g':'a', 'h':'b', 'i':'c', 'j':'d'});
    df_converted['onset_s'] = df_converted['onset_s'].round(decimals = 6);
    df_converted['offset_s'] = df_converted['offset_s'].round(decimals = 6);
    df_converted.to_csv(path, header=False, index=False,sep ='\t');
    
convert_annotations_individual(annotation_location);
convert_annotations_master(annotation_location);