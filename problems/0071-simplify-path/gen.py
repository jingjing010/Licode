from genlib import *


def ref(path):
    st = []
    for part in path.split("/"):
        if part == "" or part == ".":
            continue
        if part == "..":
            if st:
                st.pop()
        else:
            st.append(part)
    return "/" + "/".join(st)


def case(p):
    return lines(s(p))


def samples():
    data = [
        ("/home/", "/home"),
        ("/home//foo/", "/home/foo"),
        ("/home/user/Documents/../Pictures", "/home/user/Pictures"),
        ("/../", "/"),
        ("/.../a/../b/c/../d/./", "/.../b/d"),
    ]
    out = []
    for p, want in data:
        assert ref(p) == want
        out.append((case(p), s(want)))
    return out


NAME_CHARS = "abcdefghijklmnopqrstuvwxyzABCXYZ0123456789_."


def rand_path(maxlen, pieces=("", ".", "..", "..", "...", "....", "a", "b")):
    res = ""
    while True:
        r = random.random()
        if r < 0.5:
            seg = random.choice(pieces)
        else:
            seg = rand_str(random.randint(1, 6), NAME_CHARS)
        nxt = res + "/" + seg
        if len(nxt) > maxlen:
            break
        res = nxt
    if res == "":
        res = "/"
    if random.random() < 0.3 and len(res) < maxlen:
        res += "/"
    return res


def cases():
    res = [
        case("/"),
        case("//////"),
        case("/."),
        case("/.."),
        case("/a/./b/../../c/"),
        case("/a//b////c/d//././/.."),
        case("/..hidden/.x/x./_/"),
        case("/" + "/".join(["..."] * 700)),
        case("/" + "a/" * 600 + "../" * 599),
        case("/" + "../" * 999),
    ]
    for m in (20, 60, 300):
        res.append(case(rand_path(m)))
    for _ in range(3):
        p = rand_path(3000)
        assert len(p) <= 3000
        res.append(case(p))
    return res
