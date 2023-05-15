import os
import pose_matching as pm
import pandas
import random


# Precision = TP / (TP + FP)
# Recall = TP / (TP + FN)

matched = []

avg_f1_per_thresh = []
avg_f2_per_thresh = []

sim = 0.6

while sim <= 0.95:

    # Pull 5 random pose for checking
    db_feature_files = os.listdir("keypt_gen/posematching/imageDB")
    for filename in db_feature_files:
        filename = filename.split('/')[-1]
    db_feature_files_jsons = os.listdir("keypt_gen/posematching/jsonDB")
    for filename in db_feature_files_jsons:
        filename = filename.split('/')[-1]
    
    pulled = random.sample(db_feature_files_jsons, 5)
    
    avg_f1_per_pull = []
    avg_f2_per_pull = []
    for item in pulled:
        pose_name = item.split('_')[0]
        result_dict = pm.matchImageJSONToImageDatabase(r"C:\Users\Reychard\Posify_Django\keypt_gen\posematching\jsonDB\\"+item, sim)

        tp = 0
        fp = 0
        fn = 0

        for pathname, acc in result_dict.items():
            pathname = pathname.split('/')[-1]
            matched.append(pathname)

            if pose_name in pathname:
                # print("TP:", pose_name, pathname)
                tp += 1
            else:
                # print("FP:", pose_name, pathname)
                fp += 1
            

        # print(matched)

        # Check all images
        db_feature_files = os.listdir("keypt_gen/posematching/imageDB")
        for filename in db_feature_files:
            filename = filename.split('/')[-1]
            if pose_name in filename and filename not in matched:
                # print("Found: {} in database, posename = {}".format(filename, pose_name))
                fn += 1


        precision =  tp / (tp + fp)
        recall = tp / (tp + fn)

        f1 = (2 * precision * recall / (precision + recall))
        f2 = (5  * precision * recall / (4 * precision + recall))

        avg_f1_per_pull.append(f1)
        avg_f2_per_pull.append(f2)
    f1_score = round(sum(avg_f1_per_pull) / len(avg_f1_per_pull), 3)
    f2_score = round(sum(avg_f2_per_pull) / len(avg_f2_per_pull), 3)

    print("Similarity: {}\nF1: {}\nF2: {}".format(sim, f1_score, f2_score))

    avg_f1_per_thresh.append(f1_score)
    avg_f2_per_thresh.append(f2_score)
    sim += 0.01


print(avg_f1_per_thresh)
print(avg_f2_per_thresh)