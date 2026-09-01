from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = "heartwise_secret_key"


# MySQL connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ancy*2106",
        database="heartwise_db"
    )


FOOD_EMOJIS = {
    "Oats": "🥣",
    "Brown Rice": "🍚",
    "Apple": "🍎",
    "Banana": "🍌",
    "Spinach": "🌿",
    "Broccoli": "🥦",
    "Lentils": "🫘",
    "Chickpeas": "🧆",
    "Almonds": "🥜",
    "Walnuts": "🌰",
    "Salmon": "🐟",
    "Grilled Chicken": "🍗",

    "Ragi": "🌾",
    "Barley": "🌾",
    "Quinoa": "🥗",
    "Guava": "🍈",
    "Papaya": "🧡",
    "Carrot": "🥕",
    "Tomato": "🍅",
    "Cucumber": "🥒",
    "Green Beans": "🫛",
    "Moong Dal": "🫘",
    "Kidney Beans": "🫘",
    "Tofu": "🍱",

    "Chia Seeds": "🌱",
    "Flax Seeds": "🌱",
    "Pumpkin Seeds": "🎃",
    "Sunflower Seeds": "🌻",

    "Low-Fat Yogurt": "🥛",
    "Low-Fat Milk": "🥛",
    "Low-Fat Paneer": "🧀",
    "Soybeans": "🫘",
    "Edamame": "🫛",
    "Egg": "🥚",
    "Sardines": "🐟",
    "Tuna": "🐟",

    "Pear": "🍐",
    "Orange": "🍊",
    "Strawberries": "🍓",
    "Blueberries": "🫐",
    "Pomegranate": "❤️",
    "Pineapple": "🍍",
    "Avocado": "🥑",
    "Sweet Potato": "🍠",
    "Cauliflower": "🥬",
    "Bell Pepper": "🫑",
    "Zucchini": "🥒",
    "Beetroot": "🥬",

    "Whole Wheat Bread": "🍞",
    "Whole Wheat Pasta": "🍝",
    "Buckwheat": "🌾",
    "Millet": "🌾",
    "Black Beans": "🫘",
    "Green Peas": "🫛",
    "Black-Eyed Peas": "🫘",
    "Split Peas": "🫛",
    "Hummus": "🧆",
    "Tempeh": "🌱",
    "Shrimp": "🦐",
    "Trout": "🐟"
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        # Check empty fields
        if not name:
            return render_template(
                "register.html",
                error="Please enter your name."
            )

        if not email:
            return render_template(
                "register.html",
                error="Please enter your email address."
            )

        if not password:
            return render_template(
                "register.html",
                error="Please enter a password."
            )

        # Hash password before storing it
        hashed_password = generate_password_hash(password)

        db = get_db_connection()
        cursor = db.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO users (name, email, password)
                VALUES (%s, %s, %s)
                """,
                (name, email, hashed_password)
            )

            db.commit()

        except mysql.connector.IntegrityError:

            db.rollback()

            cursor.close()
            db.close()

            return render_template(
                "register.html",
                error="Email already registered."
            )

        cursor.close()
        db.close()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        # Check empty fields
        if not email:

            return render_template(
                "login.html",
                error="Please enter your email address."
            )

        if not password:

            return render_template(
                "login.html",
                error="Please enter your password."
            )

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        # Find user by email only
        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE email = %s
            """,
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()
        db.close()

        # Verify hashed password
        if user and check_password_hash(
            user["password"],
            password
        ):

            session["user_id"] = user["id"]
            session["user_name"] = user["name"]

            return redirect(url_for("dashboard"))

        # Wrong email or password
        return render_template(
            "login.html",
            error="Invalid email or password."
        )

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    name = session["user_name"]

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Check whether the user has completed their profile
    cursor.execute("""
        SELECT *
        FROM user_profiles
        WHERE user_id = %s
    """, (user_id,))

    profile = cursor.fetchone()

    # Get recommended foods based on dietary preference
    recommended_foods = []

    if profile:

        dietary_preference = profile["dietary_preference"]

        if dietary_preference == "Vegetarian":
            cursor.execute("""
                SELECT
                    id,
                    food_name,
                    category,
                    dietary_type,
                    calories,
                    protein,
                    fiber,
                    sodium
                FROM foods
                WHERE heart_healthy = TRUE
                AND dietary_type IN ('Vegetarian', 'Vegan')
                ORDER BY food_name
                LIMIT 4
            """,)

        elif dietary_preference == "Vegan":
            cursor.execute("""
                SELECT
                    id,
                    food_name,
                    category,
                    dietary_type,
                    calories,
                    protein,
                    fiber,
                    sodium
                FROM foods
                WHERE heart_healthy = TRUE
                AND dietary_type = 'Vegan'
                ORDER BY food_name
                LIMIT 4
            """,)

        else:
            cursor.execute("""
                SELECT
                    id,
                    food_name,
                    category,
                    dietary_type,
                    calories,
                    protein,
                    fiber,
                    sodium
                FROM foods
                WHERE heart_healthy = TRUE
                ORDER BY food_name
                LIMIT 4
            """,)

        recommended_foods = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "dashboard.html",
        name=name,
        profile=profile,
        recommended_foods=recommended_foods,
        food_emojis=FOOD_EMOJIS
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":

        email = request.form["email"]

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()
        db.close()

        if user:
            session["reset_user_id"] = user["id"]
            return redirect(url_for("reset_password"))

        return render_template(
            "forgot_password.html",
            error="No account found with this email."
        )

    return render_template("forgot_password.html")


@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():

    if "reset_user_id" not in session:
        return redirect(url_for("forgot_password"))

    if request.method == "POST":

        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        if new_password != confirm_password:
            return render_template(
                "reset_password.html",
                error="Passwords do not match."
            )

        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute(
            "UPDATE users SET password = %s WHERE id = %s",
            (new_password, session["reset_user_id"])
        )

        db.commit()

        cursor.close()
        db.close()

        session.pop("reset_user_id", None)

        return redirect(url_for("login"))

    return render_template("reset_password.html")


@app.route("/profile", methods=["GET", "POST"])
def profile():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Get logged-in user's basic information
    cursor.execute("""
        SELECT id, name, email
        FROM users
        WHERE id = %s
    """, (user_id,))

    user = cursor.fetchone()

    # Get existing profile, if available
    cursor.execute("""
        SELECT *
        FROM user_profiles
        WHERE user_id = %s
    """, (user_id,))

    profile_data = cursor.fetchone()

    # -------------------------------------------------
    # SAVE PROFILE
    # -------------------------------------------------

    if request.method == "POST":

        age = request.form.get("age")
        gender = request.form.get("gender")
        height = request.form.get("height")
        weight = request.form.get("weight")
        activity_level = request.form.get("activity_level")
        dietary_preference = request.form.get("dietary_preference")

        # Basic validation
        if not all([
            age,
            gender,
            height,
            weight,
            activity_level,
            dietary_preference
        ]):

            cursor.close()
            db.close()

            return render_template(
                "profile.html",
                user=user,
                profile=profile_data,
                profile_exists=profile_data is not None,
                error="Please complete all profile fields."
            )

        # ---------------------------------------------
        # PROFILE ALREADY EXISTS → UPDATE
        # ---------------------------------------------

        if profile_data:

            cursor.execute("""
                UPDATE user_profiles
                SET
                    age = %s,
                    gender = %s,
                    height = %s,
                    weight = %s,
                    activity_level = %s,
                    dietary_preference = %s
                WHERE user_id = %s
            """, (
                age,
                gender,
                height,
                weight,
                activity_level,
                dietary_preference,
                user_id
            ))

            message = "Profile updated successfully! 💚"

        # ---------------------------------------------
        # NO PROFILE → CREATE
        # ---------------------------------------------

        else:

            cursor.execute("""
                INSERT INTO user_profiles
                (
                    user_id,
                    age,
                    gender,
                    height,
                    weight,
                    activity_level,
                    dietary_preference
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                user_id,
                age,
                gender,
                height,
                weight,
                activity_level,
                dietary_preference
            ))

            message = "Profile saved successfully! 💚"

        db.commit()

        # Get the newly saved profile
        cursor.execute("""
            SELECT *
            FROM user_profiles
            WHERE user_id = %s
        """, (user_id,))

        profile_data = cursor.fetchone()

        cursor.close()
        db.close()

        return render_template(
            "profile.html",
            user=user,
            profile=profile_data,
            profile_exists=True,
            message=message
        )

    # -------------------------------------------------
    # DISPLAY PROFILE
    # -------------------------------------------------

    cursor.close()
    db.close()

    return render_template(
        "profile.html",
        user=user,
        profile=profile_data,
        profile_exists=profile_data is not None
    )


@app.route("/foods")
def foods():

    if "user_id" not in session:
        return redirect(url_for("login"))

    # Get filters from URL
    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Get user's dietary preference
    cursor.execute("""
        SELECT dietary_preference
        FROM user_profiles
        WHERE user_id = %s
    """, (session["user_id"],))

    profile = cursor.fetchone()

    if not profile:
        cursor.close()
        db.close()
        return redirect(url_for("profile"))

    dietary_preference = profile["dietary_preference"]

    # Base query
    query = """
        SELECT
            id,
            food_name,
            category,
            dietary_type,
            calories,
            protein,
            fiber,
            saturated_fat,
            sodium,
            added_sugar,
            heart_healthy
        FROM foods
        WHERE heart_healthy = TRUE
        AND (
            dietary_type = %s
            OR dietary_type = 'Vegan'
        )
    """

    params = [dietary_preference]

    # Search filter
    if search:
        query += """
            AND food_name LIKE %s
        """
        params.append(f"%{search}%")

    # Category filter
    if category:
        query += """
            AND category = %s
        """
        params.append(category)

    query += """
        ORDER BY food_name
    """

    cursor.execute(query, tuple(params))

    foods = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "foods.html",
        foods=foods,
        dietary_preference=dietary_preference,
        food_emojis=FOOD_EMOJIS,
        search=search,
        selected_category=category
    )


@app.route("/food/<int:food_id>")
def food_detail(food_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Get selected food
    cursor.execute("""
        SELECT *
        FROM foods
        WHERE id = %s
        AND heart_healthy = TRUE
    """, (food_id,))

    food = cursor.fetchone()

    # Food not found
    if not food:
        cursor.close()
        db.close()
        return "Food not found.", 404

    # Get recipes for this food
    cursor.execute("""
        SELECT *
        FROM recipes
        WHERE food_id = %s
        ORDER BY id
    """, (food_id,))

    recipes = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "food_detail.html",
        food=food,
        recipes=recipes,
        food_emojis=FOOD_EMOJIS
    )


@app.route("/recipe/<int:recipe_id>")
def recipe_detail(recipe_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            r.*,
            f.food_name,
            f.category,
            f.dietary_type
        FROM recipes r
        JOIN foods f
            ON r.food_id = f.id
        WHERE r.id = %s
        """,
        (recipe_id,)
    )

    recipe = cursor.fetchone()

    cursor.close()
    db.close()

    if not recipe:
        return render_template("404.html"), 404

    return render_template(
        "recipe_detail.html",
        recipe=recipe
    )


@app.route("/meal-plan")
def meal_plan():

    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # --------------------------------------------------
    # GET USER PROFILE
    # --------------------------------------------------

    cursor.execute(
        """
        SELECT *
        FROM user_profiles
        WHERE user_id = %s
        """,
        (session["user_id"],)
    )

    profile = cursor.fetchone()

    if not profile:
        cursor.close()
        db.close()

        return redirect(url_for("profile"))

    dietary_preference = profile["dietary_preference"]
    activity_level = profile["activity_level"]

    # --------------------------------------------------
    # DIETARY FILTER
    # --------------------------------------------------

    if dietary_preference == "Vegan":

        allowed_diets = ("Vegan",)

    elif dietary_preference == "Vegetarian":

        allowed_diets = (
            "Vegetarian",
            "Vegan"
        )

    else:

        allowed_diets = (
            "Vegetarian",
            "Vegan",
            "Non-Vegetarian"
        )

    # --------------------------------------------------
    # DAILY USER SEED
    # --------------------------------------------------

    from datetime import date

    today = date.today()

    user_id = int(session["user_id"])

    # Same user + same date = same meal plan
    # Different user/date = different meal plan
    daily_seed = today.toordinal() * 1000 + user_id

    # --------------------------------------------------
    # KEEP TRACK OF USED FOODS
    # --------------------------------------------------

    used_food_ids = set()

    # --------------------------------------------------
    # GET ONE PERSONALIZED MEAL
    # --------------------------------------------------

    def get_meal(meal_type, offset):

        placeholders = ",".join(
            ["%s"] * len(allowed_diets)
        )

        # --------------------------------------------------
        # ACTIVITY-BASED SCORING
        # --------------------------------------------------

        if activity_level == "Low":

            nutrition_score = """
                (
                    (COALESCE(f.fiber, 0) * 4)
                    - (COALESCE(f.calories, 0) * 0.01)
                    - (COALESCE(f.saturated_fat, 0) * 3)
                    - (COALESCE(f.sodium, 0) * 0.01)
                    - (COALESCE(f.added_sugar, 0) * 2)
                )
            """

        elif activity_level == "High":

            nutrition_score = """
                (
                    (COALESCE(f.protein, 0) * 4)
                    + (COALESCE(f.fiber, 0) * 2)
                    + (COALESCE(f.calories, 0) * 0.01)
                    - (COALESCE(f.saturated_fat, 0) * 3)
                    - (COALESCE(f.sodium, 0) * 0.01)
                    - (COALESCE(f.added_sugar, 0) * 2)
                )
            """

        else:

            nutrition_score = """
                (
                    (COALESCE(f.protein, 0) * 2)
                    + (COALESCE(f.fiber, 0) * 3)
                    - (COALESCE(f.saturated_fat, 0) * 3)
                    - (COALESCE(f.sodium, 0) * 0.01)
                    - (COALESCE(f.added_sugar, 0) * 2)
                )
            """

        # --------------------------------------------------
        # BUILD QUERY
        # --------------------------------------------------

        if used_food_ids:

            excluded_placeholders = ",".join(
                ["%s"] * len(used_food_ids)
            )

            query = f"""
                SELECT
                    r.*,
                    f.food_name,
                    f.category,
                    f.dietary_type,
                    f.calories,
                    f.protein,
                    f.fiber,
                    f.saturated_fat,
                    f.sodium,
                    f.added_sugar,
                    f.heart_healthy,

                    (
                        {nutrition_score}
                        +
                        CASE
                            WHEN f.heart_healthy = 1 THEN 20
                            ELSE 0
                        END
                    ) AS recommendation_score

                FROM recipes r

                JOIN foods f
                    ON r.food_id = f.id

                WHERE r.meal_type = %s

                AND f.dietary_type IN ({placeholders})

                AND r.food_id NOT IN ({excluded_placeholders})

                ORDER BY
                    recommendation_score DESC,
                    RAND(%s)

                LIMIT 1
            """

            params = (
                meal_type,
                *allowed_diets,
                *used_food_ids,
                daily_seed + offset
            )

        else:

            query = f"""
                SELECT
                    r.*,
                    f.food_name,
                    f.category,
                    f.dietary_type,
                    f.calories,
                    f.protein,
                    f.fiber,
                    f.saturated_fat,
                    f.sodium,
                    f.added_sugar,
                    f.heart_healthy,

                    (
                        {nutrition_score}
                        +
                        CASE
                            WHEN f.heart_healthy = 1 THEN 20
                            ELSE 0
                        END
                    ) AS recommendation_score

                FROM recipes r

                JOIN foods f
                    ON r.food_id = f.id

                WHERE r.meal_type = %s

                AND f.dietary_type IN ({placeholders})

                ORDER BY
                    recommendation_score DESC,
                    RAND(%s)

                LIMIT 1
            """

            params = (
                meal_type,
                *allowed_diets,
                daily_seed + offset
            )

        cursor.execute(query, params)

        meal = cursor.fetchone()

        # --------------------------------------------------
        # FALLBACK
        # --------------------------------------------------

        # If all suitable foods have already been used,
        # allow a previously used food rather than leaving
        # the meal empty.
        if not meal:

            query = f"""
                SELECT
                    r.*,
                    f.food_name,
                    f.category,
                    f.dietary_type,
                    f.calories,
                    f.protein,
                    f.fiber,
                    f.saturated_fat,
                    f.sodium,
                    f.added_sugar,
                    f.heart_healthy

                FROM recipes r

                JOIN foods f
                    ON r.food_id = f.id

                WHERE r.meal_type = %s

                AND f.dietary_type IN ({placeholders})

                ORDER BY RAND(%s)

                LIMIT 1
            """

            params = (
                meal_type,
                *allowed_diets,
                daily_seed + offset + 500
            )

            cursor.execute(query, params)

            meal = cursor.fetchone()

        # --------------------------------------------------
        # SAVE SELECTED FOOD
        # --------------------------------------------------

        if meal:
            used_food_ids.add(meal["food_id"])

        return meal

    # --------------------------------------------------
    # TODAY'S PERSONALIZED MEALS
    # --------------------------------------------------

    breakfast = get_meal("Breakfast", 101)

    lunch = get_meal("Lunch", 202)

    snack = get_meal("Snack", 303)

    dinner = get_meal("Dinner", 404)

    # --------------------------------------------------
    # CLOSE DATABASE
    # --------------------------------------------------

    cursor.close()
    db.close()

    # --------------------------------------------------
    # RENDER PAGE
    # --------------------------------------------------

    return render_template(
        "meal_plan.html",
        profile=profile,
        breakfast=breakfast,
        lunch=lunch,
        snack=snack,
        dinner=dinner
    )


if __name__ == "__main__":
    app.run(debug=True)
