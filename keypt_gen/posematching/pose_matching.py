import collections
import numpy as np
import json
import os

from operator import itemgetter



db_json_data_path = 'keypt_gen/posematching/jsonDB/'


def fetch_image(FileName, imageDirPath):
    for x in os.listdir(imageDirPath):
        if FileName in x:
            return x

def parse_JSON_single_person(filename):
    with open(filename) as data_file:
        data = json.load(data_file)

    #Keypoints
    try:
        keypointsPeople1 = data["people"][-1]["pose_keypoints_2d"] # -1 for the only person in the picture
    except IndexError as ie:
        print("Error: No person detected in the picture")
        return np.ones((25,2))

    array = np.zeros((25,2))
    arrayIndex = 0

    for i in range(0, len(keypointsPeople1), 3):
        array[arrayIndex][0] = keypointsPeople1[i]
        array[arrayIndex][1] = keypointsPeople1[i+1]
        arrayIndex+=1

    return array

def matchImageJSONToImageDatabase(imageJSONPath, acc):

    model_features = parse_JSON_single_person(imageJSONPath)

    list_of_db_features = []
    db_feature_files = os.listdir("keypt_gen/posematching/jsonDB")
    for filename in db_feature_files:
        if filename.endswith(".json"):
            with open(db_json_data_path + filename) as data_file:
                data = json.load(data_file)
            try:
                _ = data["people"][-1]["pose_keypoints_2d"]
            except IndexError as ie:
                continue
            list_of_db_features.append(parse_JSON_single_person(db_json_data_path + filename))

    res = []

    for i in range(len(list_of_db_features)):
        match_result = single_person_matching_ver2(model_features, list_of_db_features[i])
        current_comparing_filename = db_feature_files[i]
        item_acc = 1-match_result.error_score

        if (item_acc >= acc):
            res.append((round(item_acc, 3), current_comparing_filename.split("_keypoints.json")[0]))

    res.sort(key=itemgetter(0), reverse=True)



    displayed_path_sim_dict = {}
    for item_acc, filename in res:
        filename = "keypt_gen/imageDB/" + str(fetch_image(filename, "keypt_gen/posematching/imageDB/"))
        displayed_path_sim_dict[filename] = item_acc

    return displayed_path_sim_dict


def single_person_matching_ver2(pose1, pose2):

    MatchResult = collections.namedtuple("MatchResult", ["match_bool", "error_score", "input_transformation"])

    def reduce_rows(list1, list2):
        ctr = 0
        adj_idx = []
        for row in list1:
            if row[0] == 0:
                adj_idx.append(ctr)
            ctr += 1
        
        for idx in adj_idx:
            list2[idx] = [0, 0]

    def feature_scaling(input):

        # min-max scaling or min-max normalization

        xmax = max(input[:, 0])
        ymax = max(input[:, 1])

        xmin = np.min(input[np.nonzero(input[:,0])]) #np.nanmin(input[:, 0])
        ymin = np.min(input[np.nonzero(input[:,1])]) #np.nanmin(input[:, 1])

        sec_x = (input[:, 0]-xmin)/(xmax-xmin)
        sec_y = (input[:, 1]-ymin)/(ymax-ymin)

        output = np.vstack([sec_x, sec_y]).T
        output[output<0] = 0
        #logger.info("out: %s", str(output))
        return output
    
    def find_transformation(model_features, input_features):

        pad = lambda x: np.hstack([x, np.ones((x.shape[0], 1))]) 
        unpad = lambda x: x[:, :-1]

        nan_indices = []

        Y = pad(model_features)
        X = pad(input_features)

        A, _, _, _ = np.linalg.lstsq(X, Y, rcond=None)
        transform = lambda x: unpad(np.dot(pad(x), A))
        input_transform = transform(input_features)

        input_transform_list  = input_transform.tolist()
        for index in nan_indices:
            input_transform_list.insert(index, [0,0])
        input_transform = np.array(input_transform_list)


        A[np.abs(A) < 1e-10] = 0  # set really small values to zero

        return (input_transform, A)

    def max_euclidean_distance(model, transformed_input):

        manhattan_distance = np.abs(model - transformed_input)

        euclidean_distance = ((manhattan_distance[:, 0]) ** 2 + manhattan_distance[:, 1] ** 2) ** 0.5

        return max(euclidean_distance)

    # Standarize the matching "Window"

    joint_num_1 = np.count_nonzero(np.count_nonzero(pose1, axis=1))
    joint_num_2 = np.count_nonzero(np.count_nonzero(pose2, axis=1))

    if joint_num_1 < joint_num_2: # We use pose 1 as the window, if pose 2 has more joint infos, we remove them so we can focus on what matters.
        reduce_rows(pose1, pose2)
    else:
        reduce_rows(pose2, pose1)


    # Normalizing
    pose1 = feature_scaling(pose1)
    pose2 = feature_scaling(pose2)


    (input_transformed, _) = find_transformation(pose1, pose2)


    max_euclidean = max_euclidean_distance(pose1, input_transformed)

    result = MatchResult(True,
                         error_score=max_euclidean,
                         input_transformation=input_transformed)
    return result