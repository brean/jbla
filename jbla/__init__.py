import json

'''
providing helper methods to easily create new animations
'''
class BlenderAnimationBuilder(dict):
    def add_to_tween(self, name, duration=100,relative=None,
                     x=None, y=None, z=None, alpha=None):
        props = {}
        if x != None:
            props['x'] = x
        if y != None:
            props['y'] = y
        if z != None:
            props['z'] = z
        if alpha != None:
            props['alpha'] = alpha
        if relative != None:
            props['relative'] = relative
        data = {
            'type': 'to',
            'duration': duration,
            'props': props
        }
        self.setdefault(name, {})
        self[name].setdefault('tween', [])
        self[name]['tween'].append(data)

    def to_json(self, indent=2):
        return json.dumps(self, indent=indent)

class BlenderAnimation(object):
    def load(self, json_file):
        if isinstance(json_file, str):
            json_file = open(json_file, 'r')
            filename = json_file.name
        else:
            filename = json_file
        self.data = json.load(json_file)

    '''
    position object in blender based on animation properties
    '''
    def position_object(self, obj, props):
        rel = 'relative' in props and props['relative']
        # if value not set do not change object location, so start
        # with last location
        x,y,z = obj.location

        x = props['x'] + x*rel if 'x' in props else x
        y = props['y'] + y*rel if 'y' in props else y
        z = props['z'] + z*rel if 'z' in props else z

        obj.location = (x, y, z)

    def animate_to(self, tween, frames, animate_objects):
        frames += tween['duration'] / 1000.0 * self.fps
        self.scene.frame_set(frames)
        for obj in animate_objects:
            self.position_object(obj, tween['props'])
            obj.keyframe_insert(data_path="location", index=-1)
        return frames


    '''
    create animation
    (you need to run this inside blender)
    '''
    def animate(self):
        assert self.data, 'please load a json file first or set data directly'
        import bpy
        self.scene = bpy.context.scene

        # calculate frames from duration
        self.fps = self.scene.render.fps / self.scene.render.fps_base

        frame_end = 0
        for name, data in self.data.items():
            animate_objects = None
            grp = bpy.data.groups.get(name)
            if grp:
                animate_objects = grp.objects
            else:
                animate_objects = [bpy.data.objects.get(name)]

            if not animate_objects:
                raise Exception('group/object not found ' + name)

            # at keyframe at start position
            frames = 0
            self.scene.frame_set(0)

            for obj in animate_objects:
                obj.keyframe_insert(data_path="location", index=-1)

            tween_types = {
                'to': self.animate_to
            }

            for tween in data['tween']:
                frames = tween_types[tween['type']](tween, frames, animate_objects)

            frame_end = max(frame_end, frames)
        self.scene.frame_end = frame_end
        self.scene.frame_set(0)
