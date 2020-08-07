def all_coins_all_years(*funcs, years=[2018,2019], coins = ['bitcoin','ethereum', 'zcash', 'litecoin']):
	for year in years:
		for coin in coins:
			for func in funcs:
				func(coin = coin, year = year)
					