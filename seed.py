import model
import csv
import datetime
# import time   

def load_users(session):

    with open('seed_data/u.user', 'rb') as csvfile:
        linereader = csv.reader(csvfile, delimiter='|')
        
        for row in linereader:
            user = model.User()
            user.id = row[0]
            user.age = row[1]
            user.zipcode = row[4]
            session.add(user)
            # print "This is user.id", user.id
        session.commit()
    # use u.user
    

def load_movies(session):
    # use u.item
    with open('seed_data/u.item','rb') as csvfile:
        linereader = csv.reader(csvfile, delimiter='|')
        
        # counter = 0
        for row in linereader:
            movie = model.Movie()
            movie.id = row[0]
            movie.name_orig = row[1]
            movie.name = movie.name_orig[0:len(movie.name_orig)-7]
            movie.name = movie.name.decode("latin-1")
            released_at = row[2]
            
            if released_at != '':
                movie.released_at = datetime.datetime.strptime(row[2], "%d-%b-%Y")

            else:
                movie.released_at = datetime.datetime.strptime("01-Jan-1900", "%d-%b-%Y")
 
            movie.imdb_url = row[4]
            movie.imdb_url = movie.imdb_url.decode("latin-1")

            session.add(movie)
        session.commit()

def load_ratings(session):
    # use u.data
    with open('seed_data/u.data', 'rb') as csvfile:
        linereader = csv.reader(csvfile, delimiter='\t')
        
        for row in linereader:
            # print "This is row", row
            rating = model.Rating()
            rating.user_id = row[0]
            rating.movie_id = row[1]
            rating.rating = row[2]
            timestamp = int(row[3])
            rating.timestamp = datetime.datetime.fromtimestamp(timestamp)
            session.add(rating)
        session.commit()
            # print "This is rating.timestamp", rating.timestamp

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(session)
    # load_movies(session)
    load_ratings(session)
    


if __name__ == "__main__":
    s= model.session
    main(s)
