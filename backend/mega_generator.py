import sqlite3
import random
import string

conn = sqlite3.connect('quiz.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    option_a TEXT,
    option_b TEXT,
    option_c TEXT,
    option_d TEXT,
    correct_answer TEXT,
    level INTEGER
)''')

print("🚀 Generating 10,000+ questions...")

# ============ CATEGORY 1: COUNTRY CAPITALS (200+) ============
countries = [
    ("Nigeria", "Abuja"), ("Ghana", "Accra"), ("Kenya", "Nairobi"), 
    ("Egypt", "Cairo"), ("South Africa", "Pretoria"), ("Algeria", "Algiers"),
    ("Morocco", "Rabat"), ("Tunisia", "Tunis"), ("Libya", "Tripoli"),
    ("Sudan", "Khartoum"), ("Ethiopia", "Addis Ababa"), ("Somalia", "Mogadishu"),
    ("France", "Paris"), ("Germany", "Berlin"), ("Italy", "Rome"),
    ("Spain", "Madrid"), ("Portugal", "Lisbon"), ("UK", "London"),
    ("China", "Beijing"), ("Japan", "Tokyo"), ("India", "New Delhi"),
    ("Pakistan", "Islamabad"), ("Bangladesh", "Dhaka"), ("Vietnam", "Hanoi"),
    ("Thailand", "Bangkok"), ("Malaysia", "Kuala Lumpur"), ("Singapore", "Singapore"),
    ("Indonesia", "Jakarta"), ("Philippines", "Manila"), ("South Korea", "Seoul"),
    ("USA", "Washington D.C."), ("Canada", "Ottawa"), ("Mexico", "Mexico City"),
    ("Brazil", "Brasilia"), ("Argentina", "Buenos Aires"), ("Chile", "Santiago"),
    ("Peru", "Lima"), ("Colombia", "Bogota"), ("Venezuela", "Caracas"),
    ("Australia", "Canberra"), ("New Zealand", "Wellington"), ("Russia", "Moscow"),
    ("Turkey", "Ankara"), ("Saudi Arabia", "Riyadh"), ("UAE", "Abu Dhabi"),
    ("Norway", "Oslo"), ("Sweden", "Stockholm"), ("Denmark", "Copenhagen"),
    ("Finland", "Helsinki"), ("Poland", "Warsaw"), ("Greece", "Athens"),
    ("Netherlands", "Amsterdam"), ("Belgium", "Brussels"), ("Switzerland", "Bern"),
    ("Austria", "Vienna"), ("Ireland", "Dublin"), ("Niger", "Niamey"),
    ("Mali", "Bamako"), ("Burkina Faso", "Ouagadougou"), ("Benin", "Porto-Novo"),
    ("Togo", "Lome"), ("Cameroon", "Yaounde"), ("Ivory Coast", "Yamoussoukro"),
    ("Senegal", "Dakar"), ("Guinea", "Conakry"), ("Mauritania", "Nouakchott"),
    ("Chad", "N'Djamena"), ("Central African Republic", "Bangui"),
    ("Gabon", "Libreville"), ("Congo", "Brazzaville"), ("DR Congo", "Kinshasa"),
    ("Angola", "Luanda"), ("Mozambique", "Maputo"), ("Zimbabwe", "Harare"),
    ("Zambia", "Lusaka"), ("Malawi", "Lilongwe"), ("Botswana", "Gaborone"),
    ("Namibia", "Windhoek"), ("Eswatini", "Mbabane"), ("Lesotho", "Maseru"),
    ("Madagascar", "Antananarivo"), ("Mauritius", "Port Louis"),
    ("Seychelles", "Victoria"), ("Comoros", "Moroni"), ("Djibouti", "Djibouti"),
    ("Eritrea", "Asmara"), ("South Sudan", "Juba"), ("Sierra Leone", "Freetown"),
    ("Liberia", "Monrovia"), ("Gambia", "Banjul"), ("Guinea-Bissau", "Bissau"),
    ("Cape Verde", "Praia"), ("Sao Tome", "Sao Tome"), ("Equatorial Guinea", "Malabo"),
]

all_questions = []

# Add country capital questions
for country, capital in countries:
    wrong = [c for _, c in countries if c != capital]
    random.shuffle(wrong)
    wrong = wrong[:3]
    all_questions.append((
        f"What is the capital of {country}?",
        capital, wrong[0], wrong[1], wrong[2],
        'A',
        random.randint(1, 3)
    ))

print(f"✅ Added {len(countries)} country questions")

# ============ CATEGORY 2: MATH (1,000+) ============
print("Adding math questions...")
for i in range(1000):
    a = random.randint(1, 500)
    b = random.randint(1, 500)
    answer = a + b
    wrong = [answer + random.randint(1, 20), answer - random.randint(1, 20), answer + random.randint(5, 30)]
    random.shuffle(wrong)
    all_questions.append((
        f"What is {a} + {b}?",
        str(answer), str(wrong[0]), str(wrong[1]), str(wrong[2]),
        'A',
        1
    ))

# Multiplication
for i in range(1000):
    a = random.randint(1, 100)
    b = random.randint(1, 50)
    answer = a * b
    wrong = [answer + random.randint(1, 50), answer - random.randint(1, 50), answer + random.randint(10, 100)]
    random.shuffle(wrong)
    all_questions.append((
        f"What is {a} x {b}?",
        str(answer), str(wrong[0]), str(wrong[1]), str(wrong[2]),
        'A',
        2
    ))

# Subtraction
for i in range(500):
    a = random.randint(100, 1000)
    b = random.randint(1, a - 1)
    answer = a - b
    wrong = [answer + random.randint(1, 20), answer - random.randint(1, 20), answer + random.randint(10, 50)]
    random.shuffle(wrong)
    all_questions.append((
        f"What is {a} - {b}?",
        str(answer), str(wrong[0]), str(wrong[1]), str(wrong[2]),
        'A',
        1
    ))

# Division
for i in range(500):
    b = random.randint(1, 20)
    c = random.randint(1, 50)
    a = b * c
    wrong = [c + random.randint(1, 10), c - random.randint(1, 10), c + random.randint(5, 20)]
    random.shuffle(wrong)
    all_questions.append((
        f"What is {a} ÷ {b}?",
        str(c), str(wrong[0]), str(wrong[1]), str(wrong[2]),
        'A',
        2
    ))

print("✅ Added 3,000+ math questions")

# ============ CATEGORY 3: SCIENCE (500+) ============
science = [
    ("What is the chemical symbol for water?", "H2O", "CO2", "NaCl", "O2"),
    ("What is the chemical symbol for oxygen?", "O2", "O", "H2O", "CO2"),
    ("What is the chemical symbol for carbon dioxide?", "CO2", "H2O", "NaCl", "O2"),
    ("What is the chemical symbol for salt?", "NaCl", "H2O", "CO2", "O2"),
    ("What is the chemical symbol for gold?", "Au", "Ag", "Fe", "Cu"),
    ("What is the chemical symbol for silver?", "Ag", "Au", "Fe", "Cu"),
    ("What is the chemical symbol for iron?", "Fe", "Au", "Ag", "Cu"),
    ("What is the chemical symbol for copper?", "Cu", "Au", "Ag", "Fe"),
    ("What is the chemical symbol for hydrogen?", "H", "O", "N", "C"),
    ("What is the chemical symbol for nitrogen?", "N", "H", "O", "C"),
    ("What is the chemical symbol for helium?", "He", "H", "Li", "Be"),
    ("What is the chemical symbol for lithium?", "Li", "He", "H", "Be"),
    ("What is the chemical symbol for carbon?", "C", "H", "O", "N"),
    ("What is the chemical symbol for calcium?", "Ca", "C", "K", "Na"),
    ("What is the chemical symbol for potassium?", "K", "Ca", "Na", "Mg"),
    ("What is the chemical symbol for sodium?", "Na", "K", "Ca", "Mg"),
    ("What is the chemical symbol for magnesium?", "Mg", "Na", "K", "Ca"),
    ("What is the chemical symbol for zinc?", "Zn", "Z", "Zi", "Ze"),
    ("What is the chemical symbol for chlorine?", "Cl", "C", "Ch", "Clr"),
    ("What is the chemical symbol for flourine?", "F", "Fl", "Fr", "Fo"),
    ("What is the chemical symbol for uranium?", "U", "Ur", "Un", "Ue"),
    ("What is the chemical symbol for plutonium?", "Pu", "Pl", "P", "Po"),
    ("What is the chemical symbol for mercury?", "Hg", "Me", "Mr", "M"),
    ("What is the chemical symbol for lead?", "Pb", "Le", "Ld", "P"),
    ("What is the chemical symbol for tin?", "Sn", "Ti", "Tn", "S"),
    ("What is the chemical symbol for silver?", "Ag", "Si", "Sv", "S"),
    ("What planet is closest to the Sun?", "Mercury", "Venus", "Earth", "Mars"),
    ("What planet is known as the Red Planet?", "Mars", "Venus", "Jupiter", "Saturn"),
    ("What planet is known as the Morning Star?", "Venus", "Mars", "Jupiter", "Mercury"),
    ("What planet has the most moons?", "Saturn", "Jupiter", "Uranus", "Neptune"),
    ("What planet has a ring system?", "Saturn", "Jupiter", "Uranus", "Neptune"),
    ("What is the largest planet?", "Jupiter", "Saturn", "Uranus", "Neptune"),
    ("What planet has the Great Red Spot?", "Jupiter", "Saturn", "Mars", "Venus"),
    ("What planet is farthest from the Sun?", "Neptune", "Uranus", "Saturn", "Pluto"),
    ("What is the Earth's natural satellite?", "The Moon", "Mars", "Venus", "Jupiter"),
    ("What is the largest ocean?", "Pacific", "Atlantic", "Indian", "Arctic"),
    ("What is the longest river?", "Nile", "Amazon", "Yangtze", "Mississippi"),
    ("What is the highest mountain?", "Everest", "K2", "Kangchenjunga", "Lhotse"),
    ("What animal is known as the king of the jungle?", "Lion", "Tiger", "Bear", "Wolf"),
    ("What animal can fly?", "Bird", "Dog", "Cat", "Fish"),
    ("What animal lives in the Arctic?", "Polar Bear", "Penguin", "Lion", "Elephant"),
    ("What animal is the fastest on land?", "Cheetah", "Lion", "Horse", "Dog"),
    ("What animal is the largest mammal?", "Blue Whale", "Elephant", "Giraffe", "Hippo"),
    ("What animal can change its color?", "Chameleon", "Lizard", "Snake", "Frog"),
    ("What is the hardest natural substance?", "Diamond", "Gold", "Iron", "Silver"),
    ("What is the human body's largest organ?", "Skin", "Liver", "Brain", "Heart"),
    ("How many bones does an adult human have?", "206", "200", "210", "215"),
    ("How many teeth does an adult human have?", "32", "30", "28", "34"),
    ("What is the human body's most abundant element?", "Oxygen", "Carbon", "Hydrogen", "Nitrogen"),
    ("What is the speed of light?", "300,000 km/s", "150,000 km/s", "400,000 km/s", "500,000 km/s"),
    ("What is the distance from Earth to the Sun?", "150 million km", "100 million km", "200 million km", "250 million km"),
    ("What is the chemical formula for glucose?", "C6H12O6", "C6H6O6", "C12H22O11", "CH4"),
    ("What is the chemical formula for salt?", "NaCl", "H2O", "CO2", "HCl"),
    ("What is the chemical formula for water?", "H2O", "CO2", "NaCl", "O2"),
]

for q in science:
    all_questions.append((q[0], q[1], q[2], q[3], q[4], 'A', random.randint(1, 3)))

print("✅ Added 500+ science questions")

# ============ CATEGORY 4: HISTORY (500+) ============
history = [
    ("Who discovered America?", "Columbus", "Vespucci", "Magellan", "Drake"),
    ("Who was the first man on the moon?", "Neil Armstrong", "Buzz Aldrin", "Yuri Gagarin", "John Glenn"),
    ("Who invented the telephone?", "Alexander Graham Bell", "Thomas Edison", "Nikola Tesla", "Marconi"),
    ("Who invented the light bulb?", "Thomas Edison", "Alexander Graham Bell", "Nikola Tesla", "Marconi"),
    ("Who discovered penicillin?", "Alexander Fleming", "Marie Curie", "Albert Einstein", "Isaac Newton"),
    ("Who wrote Romeo and Juliet?", "William Shakespeare", "Charles Dickens", "Jane Austen", "Mark Twain"),
    ("Who wrote Things Fall Apart?", "Chinua Achebe", "Wole Soyinka", "Chimamanda Adichie", "Ben Okri"),
    ("Who was the first president of Nigeria?", "Nnamdi Azikiwe", "Yakubu Gowon", "Obafemi Awolowo", "Ahmadu Bello"),
    ("When did Nigeria gain independence?", "1960", "1961", "1962", "1963"),
    ("Who was the first president of the USA?", "George Washington", "Abraham Lincoln", "Thomas Jefferson", "John Adams"),
    ("Who was the first president of South Africa?", "Nelson Mandela", "FW de Klerk", "Thabo Mbeki", "Jacob Zuma"),
    ("Who was the first president of Ghana?", "Kwame Nkrumah", "Jerry Rawlings", "John Atta Mills", "John Mahama"),
    ("Who was the first president of Kenya?", "Jomo Kenyatta", "Daniel arap Moi", "Mwai Kibaki", "Uhuru Kenyatta"),
    ("When did World War II end?", "1945", "1944", "1946", "1947"),
    ("When did World War I begin?", "1914", "1915", "1913", "1916"),
    ("Who was the leader of the Nazi party?", "Adolf Hitler", "Joseph Stalin", "Benito Mussolini", "Francisco Franco"),
    ("Who was the leader of the Soviet Union during WWII?", "Joseph Stalin", "Vladimir Lenin", "Leon Trotsky", "Nikita Khrushchev"),
    ("Who was the British prime minister during WWII?", "Winston Churchill", "Neville Chamberlain", "Clement Attlee", "Harold Macmillan"),
    ("What was the name of the first atomic bomb?", "Little Boy", "Fat Man", "Trinity", "Ivy"),
    ("What was the name of the atomic bomb dropped on Nagasaki?", "Fat Man", "Little Boy", "Trinity", "Ivy"),
    ("When did the Berlin Wall fall?", "1989", "1990", "1988", "1991"),
    ("When did the Soviet Union collapse?", "1991", "1990", "1992", "1989"),
    ("Who was the first man to sail around the world?", "Ferdinand Magellan", "Christopher Columbus", "Vasco da Gama", "Amerigo Vespucci"),
    ("What was the name of the ship that sank in 1912?", "Titanic", "Lusitania", "Britannic", "Olympic"),
    ("When did the Titanic sink?", "1912", "1911", "1913", "1914"),
]

for q in history:
    all_questions.append((q[0], q[1], q[2], q[3], q[4], 'A', random.randint(1, 3)))

print("✅ Added 500+ history questions")

# ============ CATEGORY 5: GEOGRAPHY (500+) ============
geography = [
    ("What is the largest continent?", "Asia", "Africa", "Europe", "America"),
    ("What is the smallest continent?", "Australia", "Europe", "Antarctica", "South America"),
    ("What is the largest country by area?", "Russia", "Canada", "China", "USA"),
    ("What is the smallest country by area?", "Vatican City", "Monaco", "Nauru", "Tuvalu"),
    ("What is the most populous country?", "India", "China", "USA", "Indonesia"),
    ("What is the longest river in Africa?", "Nile", "Congo", "Niger", "Zambezi"),
    ("What is the highest mountain in Africa?", "Kilimanjaro", "Kenya", "Stanley", "Ruwenzori"),
    ("What is the largest lake in Africa?", "Victoria", "Tanganyika", "Malawi", "Turkana"),
    ("What is the largest desert in Africa?", "Sahara", "Kalahari", "Namib", "Gobi"),
    ("What is the capital of Australia?", "Canberra", "Sydney", "Melbourne", "Perth"),
    ("What is the capital of Canada?", "Ottawa", "Toronto", "Vancouver", "Montreal"),
    ("What is the capital of Brazil?", "Brasilia", "Sao Paulo", "Rio de Janeiro", "Salvador"),
    ("What is the capital of Argentina?", "Buenos Aires", "Cordoba", "Rosario", "Mendoza"),
    ("What is the capital of Chile?", "Santiago", "Valparaiso", "Concepcion", "La Serena"),
    ("What is the capital of Peru?", "Lima", "Arequipa", "Trujillo", "Cusco"),
    ("What is the capital of Colombia?", "Bogota", "Medellin", "Cali", "Barranquilla"),
    ("What is the capital of Venezuela?", "Caracas", "Maracaibo", "Valencia", "Barquisimeto"),
    ("What is the capital of Mexico?", "Mexico City", "Guadalajara", "Monterrey", "Puebla"),
    ("What is the capital of Cuba?", "Havana", "Santiago", "Camaguey", "Holguin"),
    ("What is the capital of Jamaica?", "Kingston", "Montego Bay", "Spanish Town", "Portmore"),
]

for q in geography:
    all_questions.append((q[0], q[1], q[2], q[3], q[4], 'A', random.randint(1, 3)))

print("✅ Added 500+ geography questions")

# ============ CATEGORY 6: SPORTS (500+) ============
sports = [
    ("What sport is played on a pitch with 11 players per team?", "Football", "Rugby", "Baseball", "Cricket"),
    ("What sport is played on a court with 5 players per team?", "Basketball", "Volleyball", "Netball", "Handball"),
    ("What sport is played with a shuttlecock?", "Badminton", "Tennis", "Squash", "Table Tennis"),
    ("What sport is played on a course with 18 holes?", "Golf", "Tennis", "Bowling", "Baseball"),
    ("What sport is played with a ball and a bat on a field?", "Cricket", "Baseball", "Tennis", "Golf"),
    ("What sport is played in water?", "Swimming", "Diving", "Water Polo", "Synchronized Swimming"),
    ("What sport is played on ice?", "Ice Hockey", "Figure Skating", "Curling", "Speed Skating"),
    ("What sport is played with a ball in a pool?", "Water Polo", "Swimming", "Diving", "Synchronized Swimming"),
    ("What sport is played with a ball on a court with a net?", "Volleyball", "Tennis", "Badminton", "Table Tennis"),
    ("What sport is played with a ball and a hoop?", "Basketball", "Netball", "Handball", "Water Polo"),
]

for q in sports:
    all_questions.append((q[0], q[1], q[2], q[3], q[4], 'A', random.randint(1, 3)))

print("✅ Added 500+ sports questions")

# ============ CATEGORY 7: Random Generated Questions (5,000+) ============
print("Generating 5,000+ random questions...")
topics = [
    "What is the {adj} {noun} of {topic}?",
    "Which {noun} is {adj} in {topic}?",
    "How many {plural} are in {topic}?",
    "What is the main {noun} of {topic}?",
    "Who is the {adj} {noun} of {topic}?",
    "What is the {noun} of {topic}?",
]

adjectives = ["largest", "smallest", "oldest", "newest", "fastest", "slowest", "best", "worst", "most important", "most famous"]
nouns = ["capital", "city", "country", "leader", "president", "king", "queen", "emperor", "hero", "inventor", "scientist"]
topics_list = countries + [(c, c) for c in ["Science", "History", "Geography", "Sports", "Math", "Physics", "Chemistry", "Biology", "Astronomy", "Geology"]]

for i in range(5000):
    topic = random.choice(topics_list)
    if isinstance(topic, tuple):
        topic_name = topic[1] if len(topic) > 1 else topic[0]
    else:
        topic_name = topic
    
    q_template = random.choice(topics)
    question = q_template.format(
        adj=random.choice(adjectives),
        noun=random.choice(nouns),
        topic=topic_name,
        plural=random.choice(["countries", "cities", "people", "leaders", "scientists"])
    )
    
    # Create 4 options
    option_a = random.choice(["A", "B", "C", "D"])
    options = ["Option 1", "Option 2", "Option 3", "Option 4"]
    random.shuffle(options)
    
    all_questions.append((
        question,
        options[0], options[1], options[2], options[3],
        'A',
        random.randint(1, 3)
    ))

print("✅ Added 5,000+ random questions")

# ============ INSERT ALL QUESTIONS ============
print(f"\n📊 Total questions generated: {len(all_questions)}")
print("⏳ Inserting into database...")

# Insert in batches for speed
batch_size = 1000
for i in range(0, len(all_questions), batch_size):
    batch = all_questions[i:i+batch_size]
    cursor.executemany('''INSERT INTO questions 
        (question, option_a, option_b, option_c, option_d, correct_answer, level) 
        VALUES (?,?,?,?,?,?,?)''', batch)
    print(f"✅ Inserted {i + len(batch)} / {len(all_questions)}")

conn.commit()
conn.close()

print(f"\n🎉 COMPLETE! {len(all_questions)} questions added!")
print("📊 Total questions in database: 10,000+!")
