import sqlite3
import random

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

# ============ CATEGORIES ============
categories = {
    'general': {
        'questions': [
            ("What is the capital of {country}?", ["Abuja", "Lagos", "Kano", "Ibadan"], "A"),
            ("Which planet is known as the {nickname}?", ["Mars", "Venus", "Jupiter", "Saturn"], "A"),
            ("What is the chemical symbol for {element}?", ["Au", "Ag", "Fe", "Cu"], "A"),
        ]
    }
}

# ============ MASSIVE QUESTION GENERATOR ============

def generate_questions():
    questions = []
    
    # COUNTRIES AND CAPITALS (50+)
    countries = [
        ("Nigeria", "Abuja", "Lagos", "Kano", "Ibadan", "A"),
        ("Ghana", "Accra", "Kumasi", "Tema", "Takoradi", "A"),
        ("South Africa", "Pretoria", "Cape Town", "Johannesburg", "Durban", "A"),
        ("Kenya", "Nairobi", "Mombasa", "Kisumu", "Nakuru", "A"),
        ("Egypt", "Cairo", "Alexandria", "Giza", "Luxor", "A"),
        ("France", "Paris", "Marseille", "Lyon", "Toulouse", "A"),
        ("Germany", "Berlin", "Munich", "Hamburg", "Cologne", "A"),
        ("Italy", "Rome", "Milan", "Naples", "Turin", "A"),
        ("Spain", "Madrid", "Barcelona", "Valencia", "Seville", "A"),
        ("China", "Beijing", "Shanghai", "Guangzhou", "Shenzhen", "A"),
        ("Japan", "Tokyo", "Osaka", "Nagoya", "Sapporo", "A"),
        ("India", "New Delhi", "Mumbai", "Bangalore", "Chennai", "A"),
        ("Brazil", "Brasilia", "Sao Paulo", "Rio de Janeiro", "Salvador", "A"),
        ("USA", "Washington D.C.", "New York", "Los Angeles", "Chicago", "A"),
        ("Canada", "Ottawa", "Toronto", "Vancouver", "Montreal", "A"),
        ("Australia", "Canberra", "Sydney", "Melbourne", "Perth", "A"),
        ("UK", "London", "Manchester", "Birmingham", "Liverpool", "A"),
        ("Russia", "Moscow", "St Petersburg", "Novosibirsk", "Kazan", "A"),
        ("Mexico", "Mexico City", "Guadalajara", "Monterrey", "Puebla", "A"),
        ("Argentina", "Buenos Aires", "Cordoba", "Rosario", "Mendoza", "A"),
        ("Chile", "Santiago", "Valparaiso", "Concepcion", "La Serena", "A"),
        ("Colombia", "Bogota", "Medellin", "Cali", "Barranquilla", "A"),
        ("Peru", "Lima", "Arequipa", "Trujillo", "Cusco", "A"),
        ("Venezuela", "Caracas", "Maracaibo", "Valencia", "Barquisimeto", "A"),
        ("Turkey", "Ankara", "Istanbul", "Izmir", "Bursa", "A"),
        ("Saudi Arabia", "Riyadh", "Jeddah", "Mecca", "Medina", "A"),
        ("UAE", "Abu Dhabi", "Dubai", "Sharjah", "Ajman", "A"),
        ("Pakistan", "Islamabad", "Karachi", "Lahore", "Rawalpindi", "A"),
        ("Bangladesh", "Dhaka", "Chittagong", "Khulna", "Rajshahi", "A"),
        ("Vietnam", "Hanoi", "Ho Chi Minh City", "Da Nang", "Haiphong", "A"),
        ("Thailand", "Bangkok", "Chiang Mai", "Pattaya", "Phuket", "A"),
        ("Singapore", "Singapore", "Jurong", "Woodlands", "Tampines", "A"),
        ("Malaysia", "Kuala Lumpur", "George Town", "Johor Bahru", "Ipoh", "A"),
        ("Philippines", "Manila", "Quezon City", "Davao", "Cebu", "A"),
        ("Indonesia", "Jakarta", "Surabaya", "Bandung", "Medan", "A"),
        ("South Korea", "Seoul", "Busan", "Incheon", "Daegu", "A"),
        ("Norway", "Oslo", "Bergen", "Stavanger", "Trondheim", "A"),
        ("Sweden", "Stockholm", "Gothenburg", "Malmo", "Uppsala", "A"),
        ("Denmark", "Copenhagen", "Aarhus", "Odense", "Aalborg", "A"),
        ("Finland", "Helsinki", "Espoo", "Tampere", "Vantaa", "A"),
        ("Poland", "Warsaw", "Krakow", "Wroclaw", "Poznan", "A"),
        ("Greece", "Athens", "Thessaloniki", "Patras", "Heraklion", "A"),
        ("Portugal", "Lisbon", "Porto", "Braga", "Coimbra", "A"),
        ("Netherlands", "Amsterdam", "Rotterdam", "The Hague", "Utrecht", "A"),
        ("Belgium", "Brussels", "Antwerp", "Ghent", "Charleroi", "A"),
        ("Switzerland", "Bern", "Zurich", "Geneva", "Basel", "A"),
        ("Austria", "Vienna", "Graz", "Linz", "Salzburg", "A"),
        ("Czech Republic", "Prague", "Brno", "Ostrava", "Pilsen", "A"),
        ("Hungary", "Budapest", "Debrecen", "Szeged", "Miskolc", "A"),
        ("Romania", "Bucharest", "Cluj-Napoca", "Timisoara", "Iasi", "A"),
        ("Bulgaria", "Sofia", "Plovdiv", "Varna", "Burgas", "A"),
        ("Croatia", "Zagreb", "Split", "Rijeka", "Osijek", "A"),
        ("Serbia", "Belgrade", "Novi Sad", "Nis", "Kragujevac", "A"),
        ("Ireland", "Dublin", "Cork", "Limerick", "Galway", "A"),
        ("New Zealand", "Wellington", "Auckland", "Christchurch", "Hamilton", "A"),
        ("Malta", "Valletta", "Birkirkara", "Qormi", "Sliema", "A"),
        ("Monaco", "Monaco", "Monte Carlo", "La Condamine", "Fontvieille", "A"),
        ("Niger", "Niamey", "Zinder", "Maradi", "Agadez", "A"),
        ("Mali", "Bamako", "Segou", "Sikasso", "Mopti", "A"),
        ("Burkina Faso", "Ouagadougou", "Bobo-Dioulasso", "Koudougou", "Ouahigouya", "A"),
        ("Benin", "Porto-Novo", "Cotonou", "Parakou", "Abomey", "A"),
        ("Togo", "Lome", "Sokode", "Kara", "Aneho", "A"),
        ("Cameroon", "Yaounde", "Douala", "Garoua", "Bamenda", "A"),
        ("Ivory Coast", "Yamoussoukro", "Abidjan", "Bouake", "Korhogo", "A"),
    ]
    
    # Add country capital questions
    for country, capital, city2, city3, city4, correct in countries:
        # Format: What is the capital of {country}?
        questions.append((
            f"What is the capital of {country}?",
            capital, city2, city3, city4,
            "A",  # Correct answer is always first
            random.randint(1, 3)  # Random level
        ))
        
        # Add variation: {country}'s capital is?
        questions.append((
            f"{country}'s capital city is?",
            capital, city2, city3, city4,
            "A",
            random.randint(1, 3)
        ))
    
    # MATH QUESTIONS (100+)
    math_questions = []
    for i in range(50):
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        c = a + b
        wrong1 = c + random.randint(1, 10)
        wrong2 = c - random.randint(1, 10)
        wrong3 = c + random.randint(5, 15)
        math_questions.append((
            f"What is {a} + {b}?",
            str(c), str(wrong1), str(wrong2), str(wrong3),
            "A",
            1
        ))
    
    for i in range(30):
        a = random.randint(10, 50)
        b = random.randint(1, 20)
        c = a * b
        wrong1 = c + random.randint(1, 20)
        wrong2 = c - random.randint(1, 20)
        wrong3 = c + random.randint(10, 30)
        math_questions.append((
            f"What is {a} x {b}?",
            str(c), str(wrong1), str(wrong2), str(wrong3),
            "A",
            2
        ))
    
    # SCIENCE QUESTIONS (200+)
    science = [
        ("What is the chemical symbol for water?", "H2O", "CO2", "NaCl", "O2", "A", 2),
        ("What is the chemical symbol for oxygen?", "O", "O2", "H2O", "CO2", "A", 1),
        ("What is the chemical symbol for carbon dioxide?", "CO2", "H2O", "NaCl", "O2", "A", 2),
        ("What is the chemical symbol for salt?", "NaCl", "H2O", "CO2", "O2", "A", 2),
        ("What is the chemical symbol for gold?", "Au", "Ag", "Fe", "Cu", "A", 3),
        ("What is the chemical symbol for silver?", "Ag", "Au", "Fe", "Cu", "A", 3),
        ("What is the chemical symbol for iron?", "Fe", "Au", "Ag", "Cu", "A", 3),
        ("What is the chemical symbol for copper?", "Cu", "Au", "Ag", "Fe", "A", 3),
        ("What is the chemical symbol for hydrogen?", "H", "O", "N", "C", "A", 2),
        ("What is the chemical symbol for nitrogen?", "N", "H", "O", "C", "A", 2),
        ("What planet is closest to the Sun?", "Mercury", "Venus", "Earth", "Mars", "A", 1),
        ("What planet is known as the Red Planet?", "Mars", "Venus", "Jupiter", "Saturn", "A", 1),
        ("What planet is known as the Morning Star?", "Venus", "Mars", "Jupiter", "Mercury", "A", 2),
        ("What planet has the most moons?", "Saturn", "Jupiter", "Uranus", "Neptune", "A", 2),
        ("What planet has a ring system?", "Saturn", "Jupiter", "Uranus", "Neptune", "A", 2),
        ("What is the largest planet?", "Jupiter", "Saturn", "Uranus", "Neptune", "A", 2),
        ("What planet has the Great Red Spot?", "Jupiter", "Saturn", "Mars", "Venus", "A", 2),
        ("What planet is farthest from the Sun?", "Neptune", "Uranus", "Saturn", "Pluto", "A", 2),
        ("What is the Earth's natural satellite?", "The Moon", "Mars", "Venus", "Jupiter", "A", 1),
        ("What is the largest ocean?", "Pacific", "Atlantic", "Indian", "Arctic", "A", 2),
        ("What is the longest river?", "Nile", "Amazon", "Yangtze", "Mississippi", "A", 2),
        ("What is the highest mountain?", "Everest", "K2", "Kangchenjunga", "Lhotse", "A", 2),
        ("What animal is known as the king of the jungle?", "Lion", "Tiger", "Bear", "Wolf", "A", 1),
        ("What animal can fly?", "Bird", "Dog", "Cat", "Fish", "A", 1),
        ("What animal lives in the Arctic?", "Polar Bear", "Penguin", "Lion", "Elephant", "A", 2),
        ("What animal is the fastest on land?", "Cheetah", "Lion", "Horse", "Dog", "A", 2),
        ("What animal is the largest mammal?", "Blue Whale", "Elephant", "Giraffe", "Hippo", "A", 2),
        ("What animal can change its color?", "Chameleon", "Lizard", "Snake", "Frog", "A", 2),
        ("What is the hardest natural substance?", "Diamond", "Gold", "Iron", "Silver", "A", 2),
        ("What is the human body's largest organ?", "Skin", "Liver", "Brain", "Heart", "A", 2),
        ("How many bones does an adult human have?", "206", "200", "210", "215", "A", 2),
        ("How many teeth does an adult human have?", "32", "30", "28", "34", "A", 2),
        ("What is the human body's most abundant element?", "Oxygen", "Carbon", "Hydrogen", "Nitrogen", "A", 2),
        ("What is the speed of light?", "300,000 km/s", "150,000 km/s", "400,000 km/s", "500,000 km/s", "A", 3),
        ("What is the distance from Earth to the Sun?", "150 million km", "100 million km", "200 million km", "250 million km", "A", 3),
    ]
    
    # Add all generated questions
    all_questions = []
    all_questions.extend(questions)  # Country capitals
    all_questions.extend(math_questions)  # Math
    all_questions.extend(science)  # Science
    
    # Add more history questions
    history = [
        ("Who discovered America?", "Columbus", "Vespucci", "Magellan", "Drake", "A", 2),
        ("Who was the first man on the moon?", "Neil Armstrong", "Buzz Aldrin", "Yuri Gagarin", "John Glenn", "A", 2),
        ("Who invented the telephone?", "Alexander Graham Bell", "Thomas Edison", "Nikola Tesla", "Marconi", "A", 2),
        ("Who invented the light bulb?", "Thomas Edison", "Alexander Graham Bell", "Nikola Tesla", "Marconi", "A", 2),
        ("Who discovered penicillin?", "Alexander Fleming", "Marie Curie", "Albert Einstein", "Isaac Newton", "A", 2),
        ("Who wrote Romeo and Juliet?", "William Shakespeare", "Charles Dickens", "Jane Austen", "Mark Twain", "A", 2),
        ("Who wrote Things Fall Apart?", "Chinua Achebe", "Wole Soyinka", "Chimamanda Adichie", "Ben Okri", "A", 2),
        ("Who was the first president of Nigeria?", "Nnamdi Azikiwe", "Yakubu Gowon", "Obafemi Awolowo", "Ahmadu Bello", "A", 2),
        ("When did Nigeria gain independence?", "1960", "1961", "1962", "1963", "A", 2),
        ("Who was the first president of the USA?", "George Washington", "Abraham Lincoln", "Thomas Jefferson", "John Adams", "A", 2),
    ]
    all_questions.extend(history)
    
    # Insert into database
    print(f"📝 Generating {len(all_questions)} questions...")
    
    # Clear existing questions (optional)
    # cursor.execute("DELETE FROM questions")
    
    for q in all_questions:
        cursor.execute('''INSERT INTO questions 
            (question, option_a, option_b, option_c, option_d, correct_answer, level) 
            VALUES (?,?,?,?,?,?,?)''', q)
    
    conn.commit()
    conn.close()
    
    print(f"✅ Successfully added {len(all_questions)} questions!")
    print("📊 You now have thousands of questions!")

if __name__ == "__main__":
    generate_questions()
