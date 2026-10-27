#- The code starts by importing the 'chromadb' library, which is used for database operations.
#• Then, it imports the 'Settings' class from 'chromadb.config', which is used to configure the database.
#• A 'chromadb' client is created by calling the 'Client' constructor from the 'chromadb' library.
#• The 'Client' constructor is passed a 'Settings' object as an argument.
#• The 'Settings' object is initialized with two parameters: 'chroma_db_impl' and 'persist_directory'.
#• 'chroma_db_impl' is set to "duckdb+parquet", which specifies the type of database implementation to use.
#• 'persist_directory' is set to "db/", which specifies the directory where the database files will be stored.

import chromadb
from chromadb.config import Settings

client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet",
                                    persist_directory="db/"
                                ))
#-------------------------------------------------------------------------------

#The text above is a code output or a data entry that complements the tutorial.

collection = client.create_collection(name="Students")

#------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------------------------
#- The code is using the add method of a collection object.
#• The add method is being called with three arguments: documents, metadatas, and ids.
#• documents is a list of three items: student_info, club_info, and university_info.
#• metadatas is a list of dictionaries, each containing a single key-value pair.
#• The key in each dictionary is source, and the corresponding values are "student info", "club info", and "university info".
#• ids is a list of strings: "id1", "id2", and "id3".
#• Each document is being associated with a metadata and an id, in the order they are listed.
#• This code is likely used to add documents to a database or a search index, with metadata and unique identifiers.

student_info = """
Alexandra Thompson, a 19-year-old computer science sophomore with a 3.7 GPA,
is a member of the programming and chess clubs who enjoys pizza, swimming, and hiking
in her free time in hopes of working at a tech company after graduating from the University of Washington.
"""

club_info = """
The university chess club provides an outlet for students to come together and enjoy playing
the classic strategy game of chess. Members of all skill levels are welcome, from beginners learning
the rules to experienced tournament players. The club typically meets a few times per week to play casual games,
participate in tournaments, analyze famous chess matches, and improve members' skills.
"""

university_info = """
The University of Washington, founded in 1861 in Seattle, is a public research university
with over 45,000 students across three campuses in Seattle, Tacoma, and Bothell.
As the flagship institution of the six public universities in Washington state,
UW encompasses over 500 buildings and 20 million square feet of space,
including one of the largest library systems in the world.
"""
#----------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------
 #The code starts by calling the query method on an object named collection.
#• The query method is passed two arguments: query_texts and n_results.
#• query_texts is a list containing the string "What is the student name?".
#• n_results is set to 2, indicating that the method should return the top 2 results.
#• The results of the query are stored in the variable results.
#• Finally, results is called to display the output of the query.
collection.add(
    documents = [student_info, club_info, university_info],
    metadatas = [{"source": "student info"},{"source": "club info"},{'source':'university info'}],
    ids = ["id1", "id2", "id3"]
)
#----------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------
#The text above is a code output or a data entry that complements the tutorial.

results = collection.query(
    query_texts=["What is the student name?"],
    n_results=2
)

results
#---------------------------------------------------------------------------------



