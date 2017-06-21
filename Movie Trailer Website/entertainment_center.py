import media
import fresh_tomatoes

toy_story = media.Movie('Toy Story', 'A story of a boy and his toys that come to life', 'https://images-production.global.ssl.fastly.net/uploads/posts/image/46533/toy-story-hotel.jpg', 'https://www.youtube.com/watch?v=KYz2wyBy3kc')

avatar = media.Movie('Avatar', 'A marine on an alien planet', 'https://images-na.ssl-images-amazon.com/images/M/MV5BMTYwOTEwNjAzMl5BMl5BanBnXkFtZTcwODc5MTUwMw@@._V1_UY1200_CR90,0,630,1200_AL_.jpg', 'https://www.youtube.com/watch?v=5PSNL1qE6VY')

thor = media.Movie('Thor', 'Thor is a 2011 American superhero film based on the Marvel Comics', 'http://az616578.vo.msecnd.net/files/2016/10/30/636134442114035375-463527952_thor.jpg', 'https://www.youtube.com/watch?v=JOddp-nlNvQ')

ironman = media.Movie('Ironman', 'A fictional story of wealthy business magnate, playboy and ingenious engineer', 'http://wallpapersin4k.net/wp-content/uploads/2017/02/Iron-Man-Movie-Wallpapers-2.jpg', 'https://www.youtube.com/watch?v=8hYlB38asDY')

baywatch = media.Movie('Baywatch', 'Movie captures the lives of a team of lifeguards', 'https://static1.squarespace.com/static/51b3dc8ee4b051b96ceb10de/t/587570fc3e00be27330f8f57/1484091658647/photos-from-the-baywatch-movie-2017-calendar-will-make-you-want-to-hit-the-gym', 'https://www.youtube.com/watch?v=nZ5tqzw841s')

wonderwoman = media.Movie('Wonder Woman', 'How princess Diana discovers her full powers and true destiny', 'http://t1.gstatic.com/images?q=tbn:ANd9GcQcCAOmt-FsRsR8GebIzI67qSvdQ2JLYDRLxeAcbH-541fzqq1H', 'https://www.youtube.com/watch?v=VSB4wGIdDwo')

movies = [toy_story, avatar, thor, ironman, baywatch, wonderwoman]
fresh_tomatoes.open_movies_page(movies)
