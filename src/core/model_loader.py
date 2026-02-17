def load_obj(filename: str) -> list[float]:
    # le um arquivo .obj e retorna uma lista plana de floats
    raw_vertices = []
    raw_uvs = []
    raw_normals = []
    final_buffer = []

    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue

            parts = line.split()
            if not parts:
                continue

            prefix = parts[0]
            data = parts[1:]

            if prefix == 'v':
                raw_vertices.append(list(map(float, data[:3])))
            elif prefix == 'vt':
                raw_uvs.append(list(map(float, data[:2])))
            elif prefix == 'vn':
                raw_normals.append(list(map(float, data[:3])))
            elif prefix == 'f':
                for face_vertex_str in data[:3]:
                    _process_face_vertex(
                        face_vertex_str,
                        raw_vertices,
                        raw_uvs,
                        raw_normals,
                        final_buffer
                    )

    return final_buffer


def _process_face_vertex(vertex_str, vertices, uvs, normals, output_list):
    components = vertex_str.split('/')

    v_idx = int(components[0]) - 1
    output_list.extend(vertices[v_idx])

    if len(components) > 2 and components[2]:
        n_idx = int(components[2]) - 1
        output_list.extend(normals[n_idx])
    else:
        output_list.extend([0.0, 0.0, 0.0])

    if len(components) > 1 and components[1]:
        uv_idx = int(components[1]) - 1
        output_list.extend(uvs[uv_idx])
    else:
        output_list.extend([0.0, 0.0])
