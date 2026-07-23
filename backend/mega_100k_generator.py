import sqlite3
import random
import string

conn = sqlite3.connect('quiz.db')
cursor = conn.cursor()

print("🔥 GENERATING 100,000+ QUESTIONS...")
print("⏳ This will take 5-10 minutes. Please wait!")

all_questions = []

# ============ CATEGORY 1: MATH (20,000) ============
print("📊 [1/10] Generating 20,000 math questions...")
for i in range(20000):
    a = random.randint(1, 999)
    b = random.randint(1, 999)
    op = random.choice(['+', '-', '*', '/'])
    
    if op == '+':
        ans = a + b
        w = [ans + random.randint(1, 99), ans - random.randint(1, 99), ans + random.randint(10, 150)]
        random.shuffle(w)
        all_questions.append((f"What is {a} + {b}?", str(ans), str(w[0]), str(w[1]), str(w[2]), 'A', 1))
    elif op == '-':
        if a < b: a, b = b, a
        ans = a - b
        w = [ans + random.randint(1, 50), ans - random.randint(1, 50), ans + random.randint(10, 100)]
        random.shuffle(w)
        all_questions.append((f"What is {a} - {b}?", str(ans), str(w[0]), str(w[1]), str(w[2]), 'A', 1))
    elif op == '*':
        a = random.randint(1, 100)
        b = random.randint(1, 50)
        ans = a * b
        w = [ans + random.randint(1, 100), ans - random.randint(1, 100), ans + random.randint(10, 200)]
        random.shuffle(w)
        all_questions.append((f"What is {a} x {b}?", str(ans), str(w[0]), str(w[1]), str(w[2]), 'A', 2))
    else:
        b = random.randint(1, 30)
        c = random.randint(1, 50)
        a = b * c
        w = [c + random.randint(1, 20), c - random.randint(1, 20), c + random.randint(10, 40)]
        random.shuffle(w)
        all_questions.append((f"What is {a} ÷ {b}?", str(c), str(w[0]), str(w[1]), str(w[2]), 'A', 2))

# ============ CATEGORY 2: COUNTRIES (10,000) ============
print("📊 [2/10] Generating 10,000 country questions...")
countries = [
    ("Nigeria", "Abuja"), ("Ghana", "Accra"), ("Kenya", "Nairobi"), ("Egypt", "Cairo"),
    ("South Africa", "Pretoria"), ("Algeria", "Algiers"), ("Morocco", "Rabat"),
    ("Tunisia", "Tunis"), ("Libya", "Tripoli"), ("Sudan", "Khartoum"),
    ("Ethiopia", "Addis Ababa"), ("Somalia", "Mogadishu"), ("France", "Paris"),
    ("Germany", "Berlin"), ("Italy", "Rome"), ("Spain", "Madrid"),
    ("Portugal", "Lisbon"), ("UK", "London"), ("China", "Beijing"),
    ("Japan", "Tokyo"), ("India", "New Delhi"), ("Pakistan", "Islamabad"),
    ("Bangladesh", "Dhaka"), ("Vietnam", "Hanoi"), ("Thailand", "Bangkok"),
    ("Malaysia", "Kuala Lumpur"), ("Singapore", "Singapore"), ("Indonesia", "Jakarta"),
    ("Philippines", "Manila"), ("South Korea", "Seoul"), ("USA", "Washington D.C."),
    ("Canada", "Ottawa"), ("Mexico", "Mexico City"), ("Brazil", "Brasilia"),
    ("Argentina", "Buenos Aires"), ("Chile", "Santiago"), ("Peru", "Lima"),
    ("Colombia", "Bogota"), ("Venezuela", "Caracas"), ("Australia", "Canberra"),
    ("New Zealand", "Wellington"), ("Russia", "Moscow"), ("Turkey", "Ankara"),
    ("Saudi Arabia", "Riyadh"), ("UAE", "Abu Dhabi"), ("Norway", "Oslo"),
    ("Sweden", "Stockholm"), ("Denmark", "Copenhagen"), ("Finland", "Helsinki"),
    ("Poland", "Warsaw"), ("Greece", "Athens"), ("Netherlands", "Amsterdam"),
    ("Belgium", "Brussels"), ("Switzerland", "Bern"), ("Austria", "Vienna"),
    ("Ireland", "Dublin"), ("Niger", "Niamey"), ("Mali", "Bamako"),
    ("Burkina Faso", "Ouagadougou"), ("Benin", "Porto-Novo"), ("Togo", "Lome"),
    ("Cameroon", "Yaounde"), ("Ivory Coast", "Yamoussoukro"), ("Senegal", "Dakar"),
    ("Guinea", "Conakry"), ("Mauritania", "Nouakchott"), ("Chad", "N'Djamena"),
    ("Gabon", "Libreville"), ("Congo", "Brazzaville"), ("DR Congo", "Kinshasa"),
    ("Angola", "Luanda"), ("Mozambique", "Maputo"), ("Zimbabwe", "Harare"),
    ("Zambia", "Lusaka"), ("Malawi", "Lilongwe"), ("Botswana", "Gaborone"),
    ("Namibia", "Windhoek"), ("Madagascar", "Antananarivo"), ("Mauritius", "Port Louis"),
    ("Seychelles", "Victoria"), ("Comoros", "Moroni"), ("Djibouti", "Djibouti"),
    ("Eritrea", "Asmara"), ("South Sudan", "Juba"), ("Sierra Leone", "Freetown"),
    ("Liberia", "Monrovia"), ("Gambia", "Banjul"), ("Guinea-Bissau", "Bissau"),
    ("Cape Verde", "Praia"), ("Sao Tome", "Sao Tome"), ("Equatorial Guinea", "Malabo"),
]

for i in range(10000):
    country, capital = random.choice(countries)
    wrong = [c for _, c in countries if c != capital]
    random.shuffle(wrong)
    wrong = wrong[:3]
    all_questions.append((
        f"What is the capital of {country}?",
        capital, wrong[0], wrong[1], wrong[2],
        'A',
        random.randint(1, 3)
    ))

# ============ CATEGORY 3: SCIENCE (15,000) ============
print("📊 [3/10] Generating 15,000 science questions...")
science_topics = [
    ("What planet is closest to the Sun?", "Mercury", "Venus", "Earth", "Mars"),
    ("What planet is known as the Red Planet?", "Mars", "Venus", "Jupiter", "Saturn"),
    ("What is the largest planet?", "Jupiter", "Saturn", "Uranus", "Neptune"),
    ("What planet has rings?", "Saturn", "Jupiter", "Uranus", "Neptune"),
    ("What is the chemical symbol for water?", "H2O", "CO2", "NaCl", "O2"),
    ("What is the chemical symbol for oxygen?", "O2", "O", "H2O", "CO2"),
    ("What is the chemical symbol for gold?", "Au", "Ag", "Fe", "Cu"),
    ("What is the chemical symbol for silver?", "Ag", "Au", "Fe", "Cu"),
    ("What is the chemical symbol for iron?", "Fe", "Au", "Ag", "Cu"),
    ("What is the longest river?", "Nile", "Amazon", "Yangtze", "Mississippi"),
    ("What is the highest mountain?", "Everest", "K2", "Kangchenjunga", "Lhotse"),
    ("What is the largest ocean?", "Pacific", "Atlantic", "Indian", "Arctic"),
    ("What animal is the fastest?", "Cheetah", "Lion", "Horse", "Dog"),
    ("What is the hardest natural substance?", "Diamond", "Gold", "Iron", "Silver"),
    ("How many bones in adult human?", "206", "200", "210", "215"),
    ("What is the human body's largest organ?", "Skin", "Liver", "Brain", "Heart"),
    ("What is the chemical formula for salt?", "NaCl", "H2O", "CO2", "HCl"),
    ("What is the chemical formula for methane?", "CH4", "CO2", "H2O", "NaCl"),
    ("What is the chemical formula for ammonia?", "NH3", "NO2", "H2O", "CO2"),
    ("What is the chemical formula for sulfuric acid?", "H2SO4", "HCl", "HNO3", "H3PO4"),
    ("What is the chemical formula for hydrochloric acid?", "HCl", "H2SO4", "HNO3", "H3PO4"),
    ("What is the chemical formula for sodium hydroxide?", "NaOH", "NaCl", "NaHCO3", "Na2CO3"),
    ("What is the chemical formula for baking soda?", "NaHCO3", "NaOH", "NaCl", "Na2CO3"),
    ("What is the chemical formula for calcium carbonate?", "CaCO3", "CaO", "Ca(OH)2", "CaSO4"),
]

for i in range(15000):
    q = random.choice(science_topics)
    all_questions.append((q[0], q[1], q[2], q[3], q[4], 'A', random.randint(1, 3)))

# ============ CATEGORY 4: HISTORY (10,000) ============
print("📊 [4/10] Generating 10,000 history questions...")
history_topics = [
    ("Who discovered America?", "Columbus", "Vespucci", "Magellan", "Drake"),
    ("Who was the first man on the moon?", "Neil Armstrong", "Buzz Aldrin", "Yuri Gagarin", "John Glenn"),
    ("Who invented the telephone?", "Alexander Graham Bell", "Thomas Edison", "Nikola Tesla", "Marconi"),
    ("Who invented the light bulb?", "Thomas Edison", "Alexander Graham Bell", "Nikola Tesla", "Marconi"),
    ("Who discovered penicillin?", "Alexander Fleming", "Marie Curie", "Albert Einstein", "Isaac Newton"),
    ("Who wrote Romeo and Juliet?", "William Shakespeare", "Charles Dickens", "Jane Austen", "Mark Twain"),
    ("Who wrote Things Fall Apart?", "Chinua Achebe", "Wole Soyinka", "Chimamanda Adichie", "Ben Okri"),
    ("Who was the first president of Nigeria?", "Nnamdi Azikiwe", "Yakubu Gowon", "Obafemi Awolowo", "Ahmadu Bello"),
    ("When did Nigeria gain independence?", "1960", "1961", "1962", "1963"),
    ("Who was the first president of USA?", "George Washington", "Abraham Lincoln", "Thomas Jefferson", "John Adams"),
    ("When did WWII end?", "1945", "1944", "1946", "1947"),
    ("When did WWI begin?", "1914", "1915", "1913", "1916"),
    ("Who led Nazi party?", "Adolf Hitler", "Joseph Stalin", "Benito Mussolini", "Francisco Franco"),
    ("Who was the first president of South Africa?", "Nelson Mandela", "FW de Klerk", "Thabo Mbeki", "Jacob Zuma"),
    ("Who was the first president of Ghana?", "Kwame Nkrumah", "Jerry Rawlings", "John Atta Mills", "John Mahama"),
    ("Who was the first president of Kenya?", "Jomo Kenyatta", "Daniel arap Moi", "Mwai Kibaki", "Uhuru Kenyatta"),
]

for i in range(10000):
    q = random.choice(history_topics)
    all_questions.append((q[0], q[1], q[2], q[3], q[4], 'A', random.randint(1, 3)))

# ============ CATEGORY 5: GEOGRAPHY (10,000) ============
print("📊 [5/10] Generating 10,000 geography questions...")
geography_topics = [
    ("What is the largest continent?", "Asia", "Africa", "Europe", "America"),
    ("What is the smallest continent?", "Australia", "Europe", "Antarctica", "South America"),
    ("What is the largest country by area?", "Russia", "Canada", "China", "USA"),
    ("What is the smallest country?", "Vatican City", "Monaco", "Nauru", "Tuvalu"),
    ("What is the most populous country?", "India", "China", "USA", "Indonesia"),
    ("What is the longest river in Africa?", "Nile", "Congo", "Niger", "Zambezi"),
    ("What is the highest mountain in Africa?", "Kilimanjaro", "Kenya", "Stanley", "Ruwenzori"),
    ("What is the largest desert in Africa?", "Sahara", "Kalahari", "Namib", "Gobi"),
    ("What is the capital of Australia?", "Canberra", "Sydney", "Melbourne", "Perth"),
    ("What is the capital of Canada?", "Ottawa", "Toronto", "Vancouver", "Montreal"),
    ("What is the capital of Brazil?", "Brasilia", "Sao Paulo", "Rio de Janeiro", "Salvador"),
    ("What is the capital of Argentina?", "Buenos Aires", "Cordoba", "Rosario", "Mendoza"),
]

for i in range(10000):
    q = random.choice(geography_topics)
    all_questions.append((q[0], q[1], q[2], q[3], q[4], 'A', random.randint(1, 3)))

# ============ CATEGORY 6: VOCABULARY (10,000) ============
print("📊 [6/10] Generating 10,000 vocabulary questions...")
vocab_topics = [
    ("What is the synonym of 'big'?", "Large", "Small", "Tiny", "Mini"),
    ("What is the synonym of 'fast'?", "Quick", "Slow", "Lazy", "Sluggish"),
    ("What is the synonym of 'happy'?", "Joyful", "Sad", "Upset", "Miserable"),
    ("What is the synonym of 'bright'?", "Shiny", "Dark", "Dull", "Gloomy"),
    ("What is the synonym of 'strong'?", "Powerful", "Weak", "Fragile", "Feeble"),
    ("What is the synonym of 'hard'?", "Tough", "Soft", "Gentle", "Mild"),
    ("What is the synonym of 'loud'?", "Noisy", "Quiet", "Silent", "Mute"),
    ("What is the synonym of 'new'?", "Fresh", "Old", "Ancient", "Aged"),
    ("What is the synonym of 'clean'?", "Pure", "Dirty", "Messy", "Filthy"),
    ("What is the synonym of 'rich'?", "Wealthy", "Poor", "Needy", "Struggling"),
    ("What is the opposite of 'hot'?", "Cold", "Warm", "Cool", "Freezing"),
    ("What is the opposite of 'brave'?", "Cowardly", "Afraid", "Scared", "Timid"),
    ("What is the opposite of 'kind'?", "Cruel", "Mean", "Harsh", "Unkind"),
    ("What is the opposite of 'healthy'?", "Sick", "Ill", "Unwell", "Diseased"),
    ("What is the opposite of 'young'?", "Old", "Aged", "Elderly", "Mature"),
]

for i in range(10000):
    q = random.choice(vocab_topics)
    all_questions.append((q[0], q[1], q[2], q[3], q[4], 'A', random.randint(1, 2)))

# ============ CATEGORY 7: SPORTS (5,000) ============
print("📊 [7/10] Generating 5,000 sports questions...")
sports_topics = [
    ("What sport has 11 players per team?", "Football", "Rugby", "Baseball", "Cricket"),
    ("What sport has 5 players per team?", "Basketball", "Volleyball", "Netball", "Handball"),
    ("What sport uses a shuttlecock?", "Badminton", "Tennis", "Squash", "Table Tennis"),
    ("What sport has 18 holes?", "Golf", "Tennis", "Bowling", "Baseball"),
    ("What sport is played in water?", "Swimming", "Diving", "Water Polo", "Synchronized Swimming"),
    ("What sport is played on ice?", "Ice Hockey", "Figure Skating", "Curling", "Speed Skating"),
]

for i in range(5000):
    q = random.choice(sports_topics)
    all_questions.append((q[0], q[1], q[2], q[3], q[4], 'A', random.randint(1, 3)))

# ============ CATEGORY 8: ASTRONOMY (5,000) ============
print("📊 [8/10] Generating 5,000 astronomy questions...")
astronomy_topics = [
    ("What is the closest star to Earth?", "Sun", "Proxima Centauri", "Alpha Centauri", "Sirius"),
    ("What is the largest star in the solar system?", "Sun", "Jupiter", "Saturn", "Neptune"),
    ("What is the farthest planet?", "Neptune", "Uranus", "Saturn", "Pluto"),
    ("What is the smallest planet?", "Mercury", "Mars", "Venus", "Pluto"),
    ("What is the coldest planet?", "Neptune", "Uranus", "Saturn", "Pluto"),
    ("What is the hottest planet?", "Venus", "Mercury", "Mars", "Earth"),
    ("What is the brightest star?", "Sirius", "Canopus", "Alpha Centauri", "Vega"),
    ("What is the largest moon?", "Ganymede", "Titan", "Callisto", "Io"),
    ("What is the fastest spinning planet?", "Jupiter", "Saturn", "Neptune", "Earth"),
    ("What is the slowest spinning planet?", "Venus", "Mercury", "Pluto", "Neptune"),
]

for i in range(5000):
    q = random.choice(astronomy_topics)
    all_questions.append((q[0], q[1], q[2], q[3], q[4], 'A', random.randint(2, 3)))

# ============ CATEGORY 9: TRIVIA (5,000) ============
print("📊 [9/10] Generating 5,000 trivia questions...")
trivia_topics = [
    ("What is the most common blood type?", "O", "A", "B", "AB"),
    ("What is the rarest blood type?", "AB", "O", "A", "B"),
    ("What is the smallest bone in the human body?", "Stapes", "Malleus", "Incus", "Femur"),
    ("What is the longest bone in the human body?", "Femur", "Tibia", "Fibula", "Humerus"),
    ("What is the fastest growing nail?", "Fingernail", "Toenail", "Both same", "Neither"),
    ("What is the strongest muscle?", "Masseter", "Gluteus maximus", "Heart", "Tongue"),
    ("What is the most common color in flags?", "Red", "Blue", "Green", "Yellow"),
    ("What is the rarest color in flags?", "Purple", "Pink", "Brown", "Orange"),
]

for i in range(5000):
    q = random.choice(trivia_topics)
    all_questions.append((q[0], q[1], q[2], q[3], q[4], 'A', random.randint(1, 3)))

# ============ CATEGORY 10: MASSIVE RANDOM (10,000) ============
print("📊 [10/10] Generating 10,000 random questions...")
for i in range(10000):
    a = random.randint(1, 500)
    b = random.randint(1, 500)
    c = random.randint(1, 200)
    
    templates = [
        (f"What is the square of {a}?", str(a*a), str(a*a + random.randint(1, 50)), str(a*a - random.randint(1, 50)), str(a*a + random.randint(10, 100))),
        (f"What is the cube of {a}?", str(a*a*a), str(a*a*a + random.randint(1, 100)), str(a*a*a - random.randint(1, 100)), str(a*a*a + random.randint(20, 200))),
        (f"What is {a}% of {b}?", str((a*b)//100), str((a*b)//100 + random.randint(1, 30)), str((a*b)//100 - random.randint(1, 30)), str((a*b)//100 + random.randint(10, 60))),
        (f"What is the average of {a}, {b}, and {c}?", str((a+b+c)//3), str((a+b+c)//3 + random.randint(1, 20)), str((a+b+c)//3 - random.randint(1, 20)), str((a+b+c)//3 + random.randint(10, 40))),
    ]
    q = random.choice(templates)
    all_questions.append((q[0], q[1], q[2], q[3], q[4], 'A', random.randint(1, 3)))

# ============ INSERT ALL QUESTIONS ============
print(f"\n📊 TOTAL QUESTIONS GENERATED: {len(all_questions)}")
print("⏳ Inserting into database...")

batch_size = 2000
for i in range(0, len(all_questions), batch_size):
    batch = all_questions[i:i+batch_size]
    cursor.executemany('''INSERT INTO questions 
        (question, option_a, option_b, option_c, option_d, correct_answer, level) 
        VALUES (?,?,?,?,?,?,?)''', batch)
    print(f"✅ Inserted {i + len(batch)} / {len(all_questions)}")

conn.commit()
conn.close()

print(f"\n🎉 COMPLETE! {len(all_questions)} MORE questions added!")
print("📊 Total questions in database: ~100,000+!")
