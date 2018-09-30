from algoliasearch import algoliasearch
import json

client = algoliasearch.Client("TW5OXY0XSN", '70c3a18a0229b37e26f7a31ba0d23efe')
##index1 = client.init_index('testindex1')


index = client.init_index("contacts")
batch = json.load(open('contacts.json'))
index.add_objects(batch)

index.set_settings({"customRanking": ["desc(followers)"]})

index.set_settings({"searchableAttributes": ["lastname", "firstname", "company","email", "city", "address"]})

# search by firstname
print ('searching by firstname ')
print (index.search("jimmie"))
# search a firstname with typo


print ('---------------------------------')
print (index.search("jimie"))
# search for a company

print ('---------------------------------')
print (index.search("california paint"))
# search for a firstname & company
print ('---------------------------------')
print (index.search("jimmie paint"))
