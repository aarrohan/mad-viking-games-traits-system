# =================
# === Libraries ===
# =================
import random
import json
import os

# =x=x=x=====x=x=x=

# ==============
# === Config ===
# ==============
TOTAL_METADATAS = 1000  # Number of characters you want to generate

METADATA_CHARACTER_NAME = "Random Character"  # Character name
METADATA_ASSET_TYPE = "video"  # Asset type (image or video)
METADATA_ASSET_FORMAT = "mp4"  # Asset format (ex. png, jpg, gif, mp4, mov)

POSITIVE_TRAITS_JSON_FILES_DIRECTORY = (
    "./jsons/positive-traits/"  # Directory of the positive traits json file
)

NEGATIVE_TRAITS_JSON_FILE_DIRECTORY = (
    "./jsons/"  # Directory of the negative traits json file
)
NEGATIVE_TRAITS_JSON_FILE_NAME = "negative-traits.json"  # Name of the file, that contains the negative traits of the character

METADATA_DIRECTORY_NAME = "random-character"  # Name of the directory, where the generated metadata files will be saved
# =x=x=x==x=x=x=

# ======================================
# === Negative traits json file data ===
# ======================================
negative_traits_json_file_path = (
    NEGATIVE_TRAITS_JSON_FILE_DIRECTORY + NEGATIVE_TRAITS_JSON_FILE_NAME
)

negative_traits_json_file = open(negative_traits_json_file_path, "r")
negative_traits_json_file_data = json.load(negative_traits_json_file)
# =x=x=x==========================x=x=x=


# ============================================
# === Function: Count trait weight repeats ===
# ============================================
def count_trait_weight_repeats(traits, weight):
    count = 0

    for trait in traits:
        if trait["weight"] == weight:
            count += 1

    return count


# =x=x=x================================x=x=x=

# ======================================
# === All characters positive traits ===
# ======================================
all_characters_positive_traits = []
all_characters_positive_trait_weights = []

for filename in os.listdir(POSITIVE_TRAITS_JSON_FILES_DIRECTORY):
    json_file = open(POSITIVE_TRAITS_JSON_FILES_DIRECTORY + filename, "r")
    json_file_data = json.load(json_file)

    for trait in json_file_data:
        all_characters_positive_traits.append(trait["value"].capitalize())

    for trait in json_file_data:
        totalTraitWeightRepeats = count_trait_weight_repeats(
            json_file_data, trait["weight"]
        )

        all_characters_positive_trait_weights.append(
            round(trait["weight"] / totalTraitWeightRepeats, 2)
        )

    json_file.close()
# =x=x=x==========================x=x=x=

# =================
# === Metadatas ===
# =================
metadatas = []
# =x=x=x=====x=x=x=


# =====================================
# === Function: Create new metadata ===
# =====================================
def create_new_metadata():
    new_metadata = {}

    new_metadata["edition"] = ""
    new_metadata["name"] = ""
    new_metadata["description"] = ""

    # Check metadata asset type
    if METADATA_ASSET_TYPE == "image":
        new_metadata["image"] = ""

    elif METADATA_ASSET_TYPE == "video":
        new_metadata["animation_url"] = ""

    new_metadata["attributes"] = list()

    # New positive 1 trait
    new_positive_1_trait = {}

    new_positive_1_trait["trait_type"] = "Positive 1"
    new_positive_1_trait["value"] = random.choices(
        all_characters_positive_traits, all_characters_positive_trait_weights
    )[0]

    # New positive 2 trait
    new_positive_2_trait = {}

    new_positive_2_trait["trait_type"] = "Positive 2"
    new_positive_2_trait["value"] = random.choices(
        all_characters_positive_traits, all_characters_positive_trait_weights
    )[0]

    # New negative trait
    new_choosed_negative_trait = random.choices(negative_traits_json_file_data)[0]

    new_negative_trait = {}

    new_negative_trait["trait_type"] = "Negative"
    new_negative_trait["value"] = new_choosed_negative_trait["value"]

    # Check if positive 1 trait is "Irregular"
    if new_positive_1_trait["value"] == "Irregular":
        new_positive_1_trait["value"] = random.choices(
            all_characters_positive_traits, all_characters_positive_trait_weights
        )[0]

    # Check if positive 2 trait is "Irregular"
    if new_positive_2_trait["value"] == "Irregular":
        new_positive_2_trait["value"] = random.choices(
            all_characters_positive_traits, all_characters_positive_trait_weights
        )[0]

    # Append traits inside "attributes" list
    new_metadata["attributes"].append(new_positive_1_trait)
    new_metadata["attributes"].append(new_positive_2_trait)
    new_metadata["attributes"].append(new_negative_trait)

    # Check new metadata uniqueness
    if new_metadata in metadatas:
        return create_new_metadata()

    # Check positive 1 and 2 trait values
    elif new_positive_1_trait["value"] == new_positive_2_trait["value"]:
        return create_new_metadata()

    # Check new negative trait "value" property
    elif (
        new_choosed_negative_trait["value"] == new_positive_1_trait["value"]
        or new_choosed_negative_trait["value"] == new_positive_2_trait["value"]
    ):
        return create_new_metadata()

    # Check new negative trait "antonym" property
    elif (
        new_choosed_negative_trait["antonym"] == new_positive_1_trait["value"]
        or new_choosed_negative_trait["antonym"] == new_positive_2_trait["value"]
    ):
        return create_new_metadata()

    else:
        return new_metadata


# =x=x=x=========================x=x=x=

# ========================
# === Create metadatas ===
# ========================
for i in range(TOTAL_METADATAS):
    new_metadata = create_new_metadata()

    metadatas.append(new_metadata)
# =x=x=x============x=x=x=

# ============================================
# === Add name, image, edition in metadata ===
# ============================================
edition = 1

for metadata in metadatas:
    metadata["edition"] = edition
    metadata["name"] = METADATA_CHARACTER_NAME + " #" + str(edition)

    if METADATA_ASSET_TYPE == "image":
        metadata["image"] = "ipfs://CID/" + str(edition) + "." + METADATA_ASSET_FORMAT

    elif METADATA_ASSET_TYPE == "video":
        metadata["animation_url"] = (
            "ipfs://CID/" + str(edition) + "." + METADATA_ASSET_FORMAT
        )

    edition = edition + 1
# =x=x=x================================x=x=x=

# ===============================
# === Generate metadata files ===
# ===============================
metadata_files_path = "./metadatas/" + METADATA_DIRECTORY_NAME + "/"

if os.path.exists("./metadatas/" + METADATA_DIRECTORY_NAME) == False:
    os.mkdir("./metadatas/" + METADATA_DIRECTORY_NAME)

for metadata in metadatas:
    with open(metadata_files_path + str(metadata["edition"]) + ".json", "w") as outfile:
        json.dump(metadata, outfile, indent=4)
# =x=x=x===================x=x=x=


# =========================================
# === Function: Is all metadatas unique ===
# =========================================
def isAllMetadatasUnique(metadatas):
    seen = list()

    return not any(i in seen or seen.append(i) for i in metadatas)


# =x=x=x=============================x=x=x=

# ===================
# === Close files ===
# ===================
negative_traits_json_file.close()
# =x=x=x=======x=x=x=

# ==============
# === Prints ===
# ==============
print("")

print("============ xxx ============")

print("")

print("Character Name: " + METADATA_CHARACTER_NAME)

print("")

print("---")

print("")

print("Total: " + str(TOTAL_METADATAS))

print("")

print("---")

print("")

print("Unique: " + str(isAllMetadatasUnique(metadatas)))

print("")

print("============ xxx ============")

print("")
# =x=x=x==x=x=x=
