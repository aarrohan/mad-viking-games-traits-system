# Libraries
import random
import json
import os

# Config
TOTAL_METADATAS = 100

METADATA_CHARACTER_NAME = "Berserker"
METADATA_ASSET_TYPE = "video"
METADATA_ASSET_FORMAT = "mp4"

POSITIVE_TRAITS_JSON_FILE_PATH = "./jsons/positive-traits/human-berserker.json"
METADATA_DIRECTORY_NAME = "human-berserker"
METADATA_FILE_SAVE_PATH = "./metadatas/" + METADATA_DIRECTORY_NAME + "/"

# Positive traits
positive_traits_json_file = open(POSITIVE_TRAITS_JSON_FILE_PATH, "r")
positive_traits_json_file_data = json.load(positive_traits_json_file)

# Negative traits
negative_traits_json_file = open("./jsons/negative-traits.json", "r")
negative_traits_json_file_data = json.load(negative_traits_json_file)


# Function: Count trait weight repeats
def count_trait_weight_repeats(traits, weight):
    count = 0

    for trait in traits:
        if trait["weight"] == weight:
            count += 1

    return count


# Positive 1 traits
positive_1_traits = []
positive_1_trait_weights = []

for trait in positive_traits_json_file_data:
    positive_1_traits.append(trait["value"].capitalize())

for trait in positive_traits_json_file_data:
    totalTraitWeightRepeats = count_trait_weight_repeats(
        positive_traits_json_file_data, trait["weight"]
    )

    positive_1_trait_weights.append(round(trait["weight"] / totalTraitWeightRepeats, 2))

# Positive 2 traits
positive_2_traits = []
positive_2_trait_weights = []

for trait in positive_traits_json_file_data:
    positive_2_traits.append(trait["value"].capitalize())

for trait in positive_traits_json_file_data:
    totalTraitWeightRepeats = count_trait_weight_repeats(
        positive_traits_json_file_data, trait["weight"]
    )

    positive_2_trait_weights.append(round(trait["weight"] / totalTraitWeightRepeats, 2))

# Metadatas
metadatas = []


# Function: Create new metadata
def create_new_metadata():
    new_metadata = {}

    new_metadata["edition"] = ""
    new_metadata["name"] = ""
    new_metadata["description"] = ""

    if METADATA_ASSET_TYPE == "image":
        new_metadata["image"] = ""

    elif METADATA_ASSET_TYPE == "video":
        new_metadata["animation_url"] = ""

    new_metadata["attributes"] = list()

    # New positive 1 trait
    new_positive_1_trait = {}

    new_positive_1_trait["trait_type"] = "Positive 1"
    new_positive_1_trait["value"] = random.choices(
        positive_1_traits, positive_1_trait_weights
    )[0]

    new_metadata["attributes"].append(new_positive_1_trait)

    # New positive 2 trait
    new_positive_2_trait = {}

    new_positive_2_trait["trait_type"] = "Positive 2"
    new_positive_2_trait["value"] = random.choices(
        positive_2_traits, positive_2_trait_weights
    )[0]

    new_metadata["attributes"].append(new_positive_2_trait)

    # New negative trait
    new_choosed_negative_trait = random.choices(negative_traits_json_file_data)[0]

    new_negative_trait = {}

    new_negative_trait["trait_type"] = "Negative"
    new_negative_trait["value"] = new_choosed_negative_trait["value"]

    new_metadata["attributes"].append(new_negative_trait)

    # Check new metadata uniqueness
    if new_metadata in metadatas:
        return create_new_metadata()

    # Check positive 1 and 2 trait values
    elif new_positive_1_trait["value"] == new_positive_2_trait["value"]:
        return create_new_metadata()

    # Check new negative trait 'value' property
    elif (
        new_choosed_negative_trait["value"] == new_positive_1_trait["value"]
        or new_choosed_negative_trait["value"] == new_positive_2_trait["value"]
    ):
        return create_new_metadata()

    # Check new negative trait 'antonym' property
    elif (
        new_choosed_negative_trait["antonym"] == new_positive_1_trait["value"]
        or new_choosed_negative_trait["antonym"] == new_positive_2_trait["value"]
    ):
        return create_new_metadata()

    else:
        return new_metadata


# Create metadatas
for i in range(TOTAL_METADATAS):
    new_metadata = create_new_metadata()

    metadatas.append(new_metadata)

# Add name, image, edition in metadata
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

# Generate metadata files
if os.path.exists("./metadatas/" + METADATA_DIRECTORY_NAME) == False:
    os.mkdir("./metadatas/" + METADATA_DIRECTORY_NAME)

for metadata in metadatas:
    with open(
        METADATA_FILE_SAVE_PATH + str(metadata["edition"]) + ".json", "w"
    ) as outfile:
        json.dump(metadata, outfile, indent=4)


# Function:
def isAllMetadatasUnique(metadatas):
    seen = list()

    return not any(i in seen or seen.append(i) for i in metadatas)


# Close files
positive_traits_json_file.close()

# Prints
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
