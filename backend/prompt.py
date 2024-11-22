def get_phase_one(question, essay):
    prompt = f"""
    Imagine you are an essay grader for reflection essays submitted by teachers and the question provided by the organizers as a point of reflection is
    ```Question:
    {question}
    ```

    Here is the teacher’s reflection essay:
    ```Essay:
    {essay}
    ```

    Use the criteria below to evaluate each essay based on its relevance, quality, logic, and clarity to the question demonstrated by the teacher
    ```Criteria:

    Relevance: How well does the essay show a direct and complete answer to the question?
    Presentation Quality: how well the essay was written and organized
    Logic: How well does the essay demonstrate sound reasoning, logical thinking, and coherence in its arguments?
    Clarity: How well does the essay use clear language, maintain structure, and communicate ideas effectively?
    ```

    Based on the evaluation, grade the reflection essay on a Likert Scale-based output
    Please rate each essay using the following scale:
    ```Scale:
    1 - Very Unrelated: The essay does not relate to the seminar content at all.
    2 - Unrelated: The essay has minimal connection to the seminar topics.
    3 - Somehow Unrelated: The essay touches on some seminar topics but lacks depth.
    4 - Average: The essay is somewhat relevant and demonstrates basic understanding.
    5 - Somehow Related: The essay relates to the seminar topics and shows some reflection.
    6 - Related: The essay is relevant and demonstrates good understanding and reflection.
    7 - Very Related: The essay is highly relevant, insightful, and demonstrates deep reflection on seminar content.
    ```


    Few-Shot Learning Examples
    ```Example
    Question: Which teaching strategies have you found most effective in conveying the Big Ideas in
    Mathematics to your students? Explain how you intend to implement it.


    Valid Essays:
    “Using the concrete, pictorial and abstract approach in teaching. I think I can apply this approach teaching polygons. First by showing students polygons in real-world objects, like tiles, windows, or road signs. Then students will identify and discuss the polygons they see around them. In pictorial stage, I will use charts or diagrams to illustrate different types of polygons and their properties. Then the students will draw polygons, labeling their sides and angles. Lastly, teach students the formal definitions of polygons and their properties.”
    “To teach the "Big Ideas" in math, which is super important! I'd say the most effective way is to make it relatable and engaging. Start with real-world examples: Instead of just throwing equations at students, I'd find ways to connect those ideas to their lives. Like for geometry, we could talk about how shapes are everywhere – in buildings, art, even nature! For algebra, we could use examples of how equations help us solve problems like budgeting or figuring out how much paint we need for a room. Make it interactive: I'd use games, puzzles, and activities to help students learn by doing. For example, we could play a game where they have to use their knowledge of fractions to divide a pizza fairly. Or, we could create a model of a city using blocks and then use geometric concepts to calculate its volume.”
    “To convey big ideas in Mathematics to my students, i will first explain each small parts of the big idea to them, to let students see and realize the significance of each and every part, making the big idea more understandable. I will also use models to abstract, applying inductive method.”

    Invalid:
    “Scaffolding”
    “All of the above”
    “Some of the most effective teaching strategies for conveying the Big Ideas in Mathematics include:
    1. Conceptual Understanding through Visual Models
    How it works: Using visual models like number lines, graphs, and geometric shapes helps students see the abstract concepts in a tangible way. For instance, when teaching fractions, visual aids like pie charts or fraction bars canclarify the relationship between the parts and the whole.

    Implementation: I would integrate visual tools in almost every lesson, starting with simple concepts like addition and moving to more complex ideas like algebra. For example, when introducing quadratic equations, I’d use graphs to show how the equation models a parabola, helping students connect the algebraic and geometric representations.”
    ```

    Submission Instructions
    ```
    Read each essay carefully.
    Use the grading criteria to evaluate the essay.
    Provide a score based on the Likert scale
    Output: Just give the Likert scale score (a number from 1-7).
    ```

    Make sure to just provide the score as a number. No further explanations needed. I just need the number.
    """

    return prompt


def get_phase_two(question, essay, source_material):
    prompt = f"""
        Imagine you are an essay grader for reflection essays submitted by teachers and the question provided by the organizers as a point of reflection is
        ```Question:
        {question}
        ```

        Here is the teacher’s reflection essay:
        ```Essay:
        {essay}
        ```
        Use the criteria below to evaluate each essay by comparing it with the source material if it is relevant or not. 

        ***Criteria:

        Evidence from Source Material:
        How well does the essay use relevant, accurate, and well-integrated evidence based on the speaker's deck and webinar video?

        Here is the source material: 
        ```
        {source_material}
        ```

        Based on the evaluation, grade the reflection essay on a Likert Scale-based output
        Please rate each essay using the following scale:
        ```
        1 - Very Unrelated: The essay does not relate to the seminar content at all.
        2 - Unrelated: The essay has minimal connection to the seminar topics.
        3 - Somehow Unrelated: The essay touches on some seminar topics but lacks depth.
        4 - Average: The essay is somewhat relevant and demonstrates basic understanding.
        5 - Somehow Related: The essay relates to the seminar topics and shows some reflection.
        6 - Related: The essay is relevant and demonstrates good understanding and reflection.
        7 - Very Related: The essay is highly relevant, insightful, and demonstrates deep reflection on seminar content.

        Submission Instructions
        ```
        Read each essay carefully.
        Use the grading criteria to evaluate the essay.
        Provide a score based on the Likert scale
        Important: The only output should be the Likert scale score (a number from 1-7).
    ```
    """

    return prompt
