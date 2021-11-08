df[‘new col’] = df.grouby(‘col’)[‘value’].transform(lambda x: np.count_nonzero(x))
