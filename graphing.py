import graphviz

shape = graphviz.Graph(comment="Team Composition")

shape.node("A", "Our Team")
shape.node("B", "Aziz")
shape.node("C", "Dawoud")
shape.node("D", "Islam")
shape.node("E", "George")
shape.node("F", "Moamen")
shape.node("G", "Amr")
shape.edges(['AB', 'AC', "AD", 'AE', "AF", "AG"])

shape.render('testing.png', view=True)