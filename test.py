from exacting import Exact


class Person(Exact):
    name: str
    age: int


d = Person.exact_from_json(
    """
{
    /*
        hell yeah!
    */
    name: "Walter",
    age: 23, // <- yeah, just do whatever!
}
""",
    strict=False,
)
print(d)
