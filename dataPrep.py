import pandas as pd
import ast


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
    #df.loc[df['id'] == idx]
    products_and_ingredients['id2'] = products_and_ingredients['id']
    products_and_ingredients = products_and_ingredients.drop(['id'], axis = 1)
    products_and_ingredients = products_and_ingredients.rename(columns={'index': 'id'})
    return (products_and_ingredients)

def getScores(list_of_values, ings):
    ingScores = ings[ings['ingredient'].isin(list_of_values)]
    ingScores = ingScores.iloc[0:, 0:2]
    ingScores['toxLowrisk'] = 0
    ingScores['toxMedRisk'] = 0
    ingScores['toxHighRisk'] = 0
    ingScores['toxNA'] = 0
    ingScores = ingScores.reset_index()

    for index, row in ingScores.iterrows():
        #print(ingScores.iloc[index,1])
        if ingScores.iloc[index,2] > 0 and ingScores.iloc[index,2] < 4:
            ingScores.loc[index, 'toxLowrisk'] = 1
            #print('low risk')
        elif ingScores.iloc[index,2] > 3 and ingScores.iloc[index,2] < 7:
            ingScores.loc[index, 'toxMedRisk'] = 1
            #print('med risk')
        elif ingScores.iloc[index,2] > 6:
            ingScores.loc[index, 'toxHighRisk'] = 1
            #print('med risk')       
        else:
            ingScores.loc[index, 'toxNA'] = 1

    toxLowrisk = ingScores['toxLowrisk'].sum()/len(ingScores)
    toxMedRisk = ingScores['toxMedRisk'].sum()/len(ingScores)
    toxHighRisk = ingScores['toxHighRisk'].sum()/len(ingScores)
    toxNA = ingScores['toxNA'].sum()/len(ingScores)
    return [toxLowrisk, toxMedRisk, toxHighRisk, toxNA]