def for_range(name, begin, end, step=1):  # вместо цикла написали ещё один декоратор
    def decorator(foo):  # декоратор передаем функцию foo
        def decorated(*args, **kwargs):  # оболочка декоратора, которая принимает на вход все значения функции
            if not kwargs:
                kwargs = {}
            results = []  # создали пустой список
            for i in range(begin, end, step):  # принимаем границы цикла из декоратора
                kwargs[name] = i
                results.append(foo(*args, **kwargs))  # все аргументы функции записываем в results
            return results

        return decorated

    return decorator


@for_range('i', 1, 100)
def foo(i):
    print(i)  # выводим цифры от 1 до 100

# foo()
