import pandas as pd
import umap
import os
from scripts import plotly_handler
from pathlib import Path


def generate_umap(matrix_values, matrix_lineage, to_csv, port, colorscale, opacity, n_neighbors, min_dist, spread, seed, list_lineage_order):
    # UMAP
    reducer = umap.UMAP(
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        spread=spread,
        random_state=seed
    )
    # scaled_penguin_data = StandardScaler().fit_transform(features)
    transformed_data = reducer.fit_transform(matrix_values)

    # creates matrix with all necessary information
    indexes = list(matrix_values.index.values) # List with indices corresponding to the rows of transformed_data
    matrix_of_wisdom = pd.DataFrame(indexes)

    # assigns the organisms their corresponding rank names
    for categorizeRank in list_lineage_order:
        info_of_label = []
        for el in matrix_of_wisdom.loc[:,0]:
            info_of_label.append(matrix_lineage.loc[categorizeRank][el])
        info_of_label = pd.DataFrame(info_of_label)
        matrix_of_wisdom[categorizeRank] = info_of_label

    # Adds positional matrix to label matrix
    matrix_of_wisdom["x"] = transformed_data[:, 0]
    matrix_of_wisdom["y"] = transformed_data[:, 1]

    # adds the name of species
    info_of_label = []
    for el in matrix_of_wisdom.loc[:, 0]:
        info_of_label.append(matrix_lineage.loc["species"][el])
    info_of_label = pd.DataFrame(info_of_label)
    matrix_of_wisdom["species_name"] = info_of_label

    # writes data used for plot generation to matrix
    if to_csv is True:
        path_from_root = Path(__file__).parent.parent
        path_resluts = os.path.join(path_from_root, "results/matrixdata.txt")
        matrix_of_wisdom.to_csv(path_resluts, sep="\t", index=False)

    plotly_handler.create_diagramm(matrix_of_wisdom, port, colorscale, opacity, list_lineage_order)


# Debugging purposes
if __name__ == "__main__":
    generate_umap(pd.DataFrame(), pd.DataFrame(), to_csv=False, port=8050, colorscale="Rainbow")