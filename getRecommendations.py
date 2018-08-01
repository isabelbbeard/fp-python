import pandas as pd

# Function that takes in product name as input and outputs most similar products
def get_recommendations(df, product, sim_matrix, column = 'product'):
    # Get the index of the product that matches the product name
    indices = pd.Series(df.index, index=df[column]).drop_duplicates()
    idx = indices[product]

    # Get the pairwsie similarity scores of all products with that product
    sim_scores = list(enumerate(sim_matrix[idx]))

    # Sort the products based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar products
    sim_scores = sim_scores[1:11]

    # Get the product indices
    product_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar products and their ingredients
    return df[['product', 'ingList']].iloc[product_indices]