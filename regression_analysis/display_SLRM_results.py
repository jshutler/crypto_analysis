from statsmodels.regression.linear_model import OLSResults
from os import listdir
import pandas as pd 


def main(models):
	#models is the list of model names
	r_squareds = []
	coefficients = []
	standerd_errors = []
	residuals = []

	for model in models:
		

		results = OLSResults.load(f'regression_models/return_predictions/{coin}/{model}')
		r_squareds.append(results.rsquared)
		coefficients.append(tuple(results.params))
		standerd_errors.append(tuple(results.bse))
		residuals.append(results.df_resid)

		# model_dict.update({model, [results.rsquared, results.params,results.bse]})

	
	model_dict = {'r_squareds': r_squareds, 'coefficients': coefficients, 'standerd_errors': standerd_errors, 'residuals': residuals}

	print(model_dict)


	model_df = pd.DataFrame(model_dict, index=models).sort_values('r_squareds', ascending=False)

	print(model_df)

	
	model_df.to_csv(f'results/return_predictions/{coin}_model_results.csv')
	print('model saved to "model_df.csv"')


if __name__ == '__main__':
	coins = ['bitcoin', 'ethereum', 'Zcash', 'litecoin']
	for coin in coins:
		models = listdir(f'regression_models/return_predictions/{coin}')
		main(models)