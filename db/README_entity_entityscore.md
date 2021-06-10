# Relevant Files: 
1. getEntities.py => has two functions:
	- to\_database: Purpose is to insert new entities into database. Will only insert if entity is not
			in database yet. 
		- Input: DataFrame and a database file name (String. Optional).
		- Output: None 
	- getEntityNameById:
		- Input: entity name (String) and a database file name (String. Optional).
		- Output: either None or entity\_name (String)
	- getEntityIdByName:
		- Input: entity name (String) and a database file name (String. Optional).
		- Output: either None or entity\_id (Integer)

2. getEntityScores.py => has three relevant functions: 
	- to\_database: Purpose is to insert entity score and query time for an entity into database. Will only insert
			if entity is already present in entity table in the given database. Otherwise a warning
			will be shown and operation is skipped (Not sure if should throw error at this point)
		- Input: DataFrame and a database file name (String)
		- Output: None
	- getEntityScore: Purpose is to get entity score/s of a given entity. This will retrieve all scores of the 
			  entity, regardless of the time field. 
		- Input: entity name (String) and a database file name (String. Optional). 
		- Output: either None or a list of tuples. The tuples are of the form: 
				(entity\_score\_id, entity\_score, date_time, entity\_id)
	- getEntityScoreAtTime: Purpose is to get entity score of a given entity at a given time.
			This will retrieve only 1 score that corresponds to the given time, or None if no data matches. 
		- Input: entity name (String), a database file name (String), and date (DD-MM-YYYY)
		- Output: either None or float.

Additional Notes: 
- Run the respective files to see their outputs and possible warnings, if any.
  Run getEntities.py first before getEntityScores.py
- DataFrame needs to have certain specific column names. Otherwise assertion error will be thrown. 
