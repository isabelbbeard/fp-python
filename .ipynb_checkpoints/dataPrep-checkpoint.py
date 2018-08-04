import pandas as pd


def dataPrep(ings, prods, prod_ing):
    #clean weird ingredient
    ings['ingredient'] = ings['ingredient'].replace('Stearic Acid(Masking, Fragrance, Emulsion Stabilising, Emulsifying, Sufactant, Refatting, Surfactantsurfactant-Cleansing Agent Is Included As A Function For The Soap Form Of Stearic Acid.', 'Stearic Acid')
    prod_ing['ingredient'] = prod_ing['ingredient'].replace('Stearic Acid(Masking, Fragrance, Emulsion Stabilising, Emulsifying, Sufactant, Refatting, Surfactantsurfactant-Cleansing Agent Is Included As A Function For The Soap Form Of Stearic Acid.', 'Stearic Acid')
    #drop duplicates
    ings = ings.drop_duplicates(subset = 'ingredient')
    
    #create a df so that each ingredient has a uniqueID
    ing_uniqueID = ings.loc[:,['ingredient']].reset_index().drop(['index'], axis = 1)
    #ing_uniqueID = ing_uniqueID.drop(['index'], axis = 1)
    ing_uniqueID['uniqueID'] = ing_uniqueID.index
    
    #Merge prod_ing and the unique ID so that each ingredient has it's unique ID
    prod_ing = pd.merge(prod_ing, ing_uniqueID, on='ingredient')
    #Sort by product id and ingredient order
    prod_ing = prod_ing.sort_values(['id','order'])

    ##now we want the ingredients to be shown as a list instead of separate cells
    prod_ing.groupby('id')['ingredient'].apply(list)
    
    ##group and create list
    prod_ing_lists = prod_ing.groupby('id')['ingredient'].apply(list)
    prod_ing_ID_lists = prod_ing.groupby('id')['uniqueID'].apply(list)

    ##convert back to dataframe and reset index
    prod_ing_df = prod_ing_lists.to_frame().reset_index()
    prod_ing_ID_df = prod_ing_ID_lists.to_frame().reset_index()
    ##check to make sure unique id's are still in tact (id shouldn't be exactly == to index)
    prod_ing_lists = pd.merge(prod_ing_df, prod_ing_ID_df, on='id')
    prod_ing_lists = prod_ing_lists.rename(columns = {'ingredient': 'ingList', 'uniqueID': 'ing#List' })
    
    ##merge ingredient lists with products
    products_and_ingredients= pd.merge(prod_ing_lists, prods, on = 'id')
    #add a column with ingredient counts
    products_and_ingredients['ingCount'] = products_and_ingredients['ingList'].apply(lambda x: len(x))
    
    #print('Number of products: ', len(products_and_ingredients))
    #print('Number of unique ingredients: ', len(ing_uniqueID))
    return (products_and_ingredients)