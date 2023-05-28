def for_range(name, enum):  # вместо цикла написали ещё один декоратор
    def decorator(foo):  # декоратору передаем функцию foo
        def decorated(*args, **kwargs):  # оболочка декоратора, которая принимает на вход все значения функции
            if not kwargs:
                kwargs = {}
            results = []  # создали пустой список
            for i in enum:  # принимаем границы цикла из декоратора
                kwargs[name] = i
                results.append(foo(*args, **kwargs))  # все аргументы функции записываем в results
            return results

        return decorated

    return decorator


@for_range('i', range(0, 100))
def foo(i):
    print(i)  # выводим цифры от 0 до 100

# foo()
