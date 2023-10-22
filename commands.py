from main import db, bcrypt
from flask import Blueprint
from models import User, BlogPost, Comment, Like, Follower, Category


# create blueprint for CLI commands
db_command = Blueprint("db", __name__)


# "flask db create" CLI command - creates database tables using SQLAlchemy
@db_command.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created...")


# "flask db drop" CLI command - removes tables from database
@db_command.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped...")


# "flask db seed" CLI command - seeds the database with information
@db_command.cli.command("seed")
def seed_db():
    # seed users
    user1 = User(
        name="Jim Parsons",
        email="jimparsons@gmail.com",
        password=bcrypt.generate_password_hash("Password.123").decode("utf-8"),
    )

    user2 = User(
        name="Lebron James",
        email="lebronjames@gmail.com",
        password=bcrypt.generate_password_hash("Password.123").decode("utf-8"),
    )

    user3 = User(
        name="Christiano Ronaldo",
        email="christianoronaldo@gmail.com",
        password=bcrypt.generate_password_hash("Password.123").decode("utf-8"),
    )

    user4 = User(
        name="Joe Biden",
        email="joebiden@gmail.com",
        password=bcrypt.generate_password_hash("Password.123").decode("utf-8"),
    )

    db.session.add_all([user1, user2, user3, user4])

    db.session.commit()

    # seed blog posts
    blogpost1 = BlogPost(
        post_title="My Experience With The Big Bang Theory",
        post_content="My journey on The Big Bang Theory was nothing short of extraordinary. Portraying Sheldon Cooper, a quirky and brilliant theoretical physicist, was an adventure filled with laughter, learning, and endless moments that will forever hold a special place in my heart. Sheldon's character was a unique challenge that pushed my acting abilities to their limits. Capturing his idiosyncrasies, from his love of comic books and video games to his struggles with social interactions, was a delightful puzzle. It was incredible to see how the audience embraced this character and found humor in his peculiarities. The camaraderie among the cast and crew was unparalleled. We became a tight-knit family, sharing countless laughs both on and off the set. Working alongside talented actors like Johnny Galecki, Kaley Cuoco, Simon Helberg, Kunal Nayyar, and the rest of the brilliant ensemble was an honor. The show's success was overwhelming, and its impact on pop culture was astonishing. I am humbled by the fans' unwavering support and their affection for Sheldon and the gang. The Big Bang Theory allowed us to explore complex scientific concepts while delivering humor that resonated with a broad audience. As I look back on my time as Sheldon, I am filled with gratitude for the incredible experience and the lifelong friendships that blossomed during those 12 remarkable seasons. It was a journey that I will cherish forever, and I thank each and every fan for being part of it. Bazinga!",
        posted_date="12-12-2012",
        updated_date="08-10-2014",
        author_id=1,
    )

    blogpost2 = BlogPost(
        post_title="Playing For The Lakers",
        post_content="Playing for the Los Angeles Lakers has been an incredible journey in my basketball career. When I first signed with the Lakers, I knew I was stepping into the footsteps of some of the greatest players in the history of the game – legends like Magic Johnson, Kareem Abdul-Jabbar, and Kobe Bryant. The weight of that legacy was something I embraced, not as pressure, but as motivation to elevate my game to new heights. The Lakers' fan base is unmatched. They bleed purple and gold, and their passion for the game is inspiring. Walking into the Staples Center on game day, you can feel the energy and excitement in the air. It's like playing in a Hollywood blockbuster every night, and I love every moment of it. One of the most fulfilling aspects of my Lakers journey has been the opportunity to play alongside incredible talents like Anthony Davis. Teaming up with AD, forming a partnership both on and off the court, has been a dream come true. We share the same hunger for success, and our chemistry has been the key to our success. Winning the NBA Championship with the Lakers was a special moment in my career. It was a testament to the hard work, dedication, and unity of our team. Bringing that championship trophy back to the Lakers faithful was a moment I'll cherish forever. I look forward to continuing this journey with the Lakers, chasing more championships, and leaving a lasting legacy in the city of angels. The Lakers' purple and gold runs through my veins, and I couldn't be prouder to be a part of this storied franchise.",
        posted_date="11-01-2016",
        updated_date="04-11-2019",
        author_id=2,
    )

    blogpost3 = BlogPost(
        post_title="Balancing Family and Football",
        post_content="Balancing the relentless demands of professional football and the joys of family life has been a journey filled with challenges and profound rewards. As a father and a footballer, finding equilibrium has been paramount in my life. My family, my rock, provides the unwavering support and motivation that fuels my on-field endeavors. From cheering in the stands to celebrating victories at home, they're the heart of my success. Being there for my children's milestones, their first steps and words, has been as exhilarating as scoring a winning goal. Yet, the demands of football are all-consuming. Training regimes, matches, travel – it can be exhausting. Maintaining a healthy work-life balance requires sacrifice and discipline. It means missing some precious moments at home. However, it's these sacrifices that strengthen my resolve to succeed both on and off the pitch. The values instilled in me by my family – dedication, hard work, and a commitment to excellence – are the same principles that drive me as an athlete. They are my driving force in achieving my goals, not just as a footballer, but as a father. So, the journey continues, with my family as my greatest supporters, and football as my passion. Balancing these two worlds is an ongoing challenge, but it's one that I embrace with all my heart, because the rewards, both as a father and a footballer, are immeasurable.",
        posted_date="09-10-2014",
        updated_date="02-03-2018",
        author_id=3,
    )

    blogpost4 = BlogPost(
        post_title="Healthcare for All: The Path Forward",
        post_content="My fellow Americans, In our great nation, access to quality healthcare should never be a privilege. It's a fundamental right that every citizen deserves. That's why, during my time in office, we have been committed to advancing the cause of healthcare for all. The Affordable Care Act, often referred to as Obamacare, was a significant step in the right direction. It expanded access to affordable healthcare for millions of Americans, protected those with pre-existing conditions, and allowed young adults to stay on their parents' insurance plans. But we recognize that there is more work to be done. Our vision for healthcare is one where no American has to choose between their health and their financial stability. It's a vision where preventive care is the norm, where the cost of prescription drugs is reasonable, and where rural communities have access to the same quality care as urban areas. To achieve this vision, we are working diligently to build upon the progress made by the Affordable Care Act. We're striving to lower healthcare costs, increase the availability of affordable insurance options, and expand Medicaid to cover more vulnerable Americans. But we can't do this alone. It's a path we must walk together as a nation. We need bipartisan cooperation and a commitment from every citizen to prioritize the health and well-being of our fellow Americans. Healthcare for all is not just a policy goal; it's a moral imperative. Together, we can forge a path forward towards a healthier, more equitable America. Thank you, and may we all enjoy good health and prosperity.",
        posted_date="04-11-2022",
        updated_date="04-11-2022",
        author_id=4,
    )

    db.session.add_all([blogpost1, blogpost2, blogpost3, blogpost4])

    db.session.commit()

    # seed comments
    comment1 = Comment(
        comment_text="Wow this is fascinating!",
        comment_date="12-12-2013",
        updated_date="05-10-2014",
        author_id=2,
        post_id=1,
    )

    comment2 = Comment(
        comment_text="Amazing post, thank you Lebron.",
        comment_date="10-11-2018",
        updated_date="11-12-2019",
        author_id=3,
        post_id=2,
    )

    comment3 = Comment(
        comment_text="Your family is beautiful!",
        comment_date="10-01-2017",
        updated_date="01-02-2018",
        author_id=1,
        post_id=3,
    )

    comment4 = Comment(
        comment_text="I love this show!",
        comment_date="10-02-2017",
        updated_date="11-07-2019",
        author_id=3,
        post_id=1,
    )

    comment5 = Comment(
        comment_text="You're a top player!",
        comment_date="11-05-2018",
        updated_date="07-08-2019",
        author_id=4,
        post_id=2,
    )

    comment6 = Comment(
        comment_text="Lovely family!",
        comment_date="11-02-2015",
        updated_date="11-04-2016",
        author_id=1,
        post_id=4,
    )

    db.session.add_all([comment1, comment2, comment3, comment4, comment5, comment6])

    db.session.commit()

    # seed likes
    like1 = Like(liker_id=1, post_id=2, comment_id=None)

    like2 = Like(liker_id=1, post_id=3, comment_id=None)

    like3 = Like(liker_id=1, post_id=None, comment_id=3)

    like4 = Like(liker_id=2, post_id=1, comment_id=None)

    like5 = Like(liker_id=3, post_id=None, comment_id=1)

    like6 = Like(liker_id=1, post_id=None, comment_id=2)

    like7 = Like(liker_id=4, post_id=None, comment_id=6)

    like8 = Like(liker_id=4, post_id=1, comment_id=None)

    like9 = Like(liker_id=3, post_id=4, comment_id=None)

    db.session.add_all([like1, like2, like3, like4, like5, like6, like7, like8, like9])

    db.session.commit()

    # seed followers
    follower1 = Follower(follower_id=1, followed_id=2)

    follower2 = Follower(follower_id=3, followed_id=1)

    follower3 = Follower(follower_id=2, followed_id=3)

    follower4 = Follower(follower_id=4, followed_id=3)

    follower5 = Follower(follower_id=3, followed_id=4)

    follower6 = Follower(follower_id=4, followed_id=1)

    db.session.add_all(
        [follower1, follower2, follower3, follower4, follower5, follower6]
    )

    db.session.commit()

    # seed categories
    category1 = Category(category_name="Sports", post_id=2)

    category2 = Category(category_name="TV", post_id=1)

    category3 = Category(category_name="Football", post_id=3)

    category4 = Category(category_name="Politics", post_id=4)

    db.session.add_all([category1, category2, category3, category4])

    db.session.commit()

    print("Database seeded...")
