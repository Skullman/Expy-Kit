

class HumanLimb:
    def __str__(self):
        return self.__class__.__name__ + ' ' + ', '.join(["{0}: {1}".format(k, v) for k, v in self.__dict__.items()])

    def __getitem__(self, item):
        return getattr(self, item, None)

    def items(self):
        return self.__dict__.items()


class HumanSpine(HumanLimb):
    def __init__(self, head='', neck='', spine2='', spine1='', spine='', hips=''):
        self.head = head
        self.neck = neck
        self.spine2 = spine2
        self.spine1 = spine1
        self.spine = spine
        self.hips = hips


class HumanArm(HumanLimb):
    def __init__(self, shoulder='', arm='', forearm='', hand=''):
        self.shoulder = shoulder
        self.arm = arm
        self.forearm = forearm
        self.hand = hand


class HumanLeg(HumanLimb):
    def __init__(self, upleg='', leg='', foot='', toe=''):
        self.upleg = upleg
        self.leg = leg
        self.foot = foot
        self.toe = toe


class HumanFingers(HumanLimb):
    def __init__(self, thumb=[''] * 3, index=[''] * 3, middle=[''] * 3, ring=[''] * 3, pinky=[''] * 3):
        self.thumb = thumb
        self.index = index
        self.middle = middle
        self.ring = ring
        self.pinky = pinky


class HumanSkeleton:
    spine = None

    left_arm = None
    right_arm = None
    left_leg = None
    right_leg = None

    left_fingers = None
    right_fingers = None

    def conversion_map(self, target_skeleton):
        """Return a dictionary that maps skeleton bone names to target bone names
        >>> rigify = RigifySkeleton()
        >>> rigify.conversion_map(MixamoSkeleton())
        {'DEF-spine.006': 'Head', 'DEF-spine.004': 'Neck', 'DEF-spine.003'...
        """
        bone_map = dict()

        def bone_mapping(attr, limb, bone_name):
            target_limbs = getattr(target_skeleton, attr, None)
            if not target_limbs:
                return

            trg_name = target_limbs[limb]

            if trg_name:
                bone_map[bone_name] = trg_name

        for limb_name, bone_name in self.spine.items():
            bone_mapping('spine', limb_name, bone_name)

        for limb_name, bone_name in self.left_arm.items():
            bone_mapping('left_arm', limb_name, bone_name)

        for limb_name, bone_name in self.right_arm.items():
            bone_mapping('right_arm', limb_name, bone_name)

        for limb_name, bone_name in self.left_leg.items():
            bone_mapping('left_leg', limb_name, bone_name)

        for limb_name, bone_name in self.right_leg.items():
            bone_mapping('right_leg', limb_name, bone_name)

        def fingers_mapping(src_fingers, trg_fingers):
            for finger, bone_names in src_fingers.items():
                trg_bone_names = trg_fingers[finger]

                assert len(bone_names) == len(trg_bone_names)
                for bone, trg_bone in zip(bone_names, trg_bone_names):
                    bone_map[bone] = trg_bone

        trg_fingers = target_skeleton.left_fingers
        fingers_mapping(self.left_fingers, trg_fingers)

        trg_fingers = target_skeleton.right_fingers
        fingers_mapping(self.right_fingers, trg_fingers)

        return bone_map


class MixamoSkeleton(HumanSkeleton):
    def __init__(self):
        self.spine = HumanSpine(
            head='Head',
            neck='Neck',
            spine2='Spine2',
            spine1='Spine1',
            spine='Spine',
            hips='Hips'
        )

        side = 'Left'
        self.left_arm = HumanArm(shoulder=side + "Shoulder",
                                 arm=side + "Arm",
                                 forearm=side + "ForeArm",
                                 hand=side + "Hand")

        self.left_fingers = HumanFingers(
                    thumb=["{0}HandThumb{1}".format(side, i) for i in range(1, 4)],
                    index=["{0}HandIndex{1}".format(side, i) for i in range(1, 4)],
                    middle=["{0}HandMiddle{1}".format(side, i) for i in range(1, 4)],
                    ring=["{0}HandRing{1}".format(side, i) for i in range(1, 4)],
                    pinky=["{0}HandPinky{1}".format(side, i) for i in range(1, 4)],
                )

        self.left_leg = HumanLeg(upleg="{0}UpLeg".format(side),
                                  leg="{0}Leg".format(side),
                                  foot="{0}Foot".format(side),
                                  toe="{0}ToeBase".format(side))

        side = 'Right'
        self.right_arm = HumanArm(shoulder=side + "Shoulder",
                                 arm=side + "Arm",
                                 forearm=side + "ForeArm",
                                 hand=side + "Hand")

        self.right_fingers = HumanFingers(
            thumb=["{0}HandThumb{1}".format(side, i) for i in range(1, 4)],
            index=["{0}HandIndex{1}".format(side, i) for i in range(1, 4)],
            middle=["{0}HandMiddle{1}".format(side, i) for i in range(1, 4)],
            ring=["{0}HandRing{1}".format(side, i) for i in range(1, 4)],
            pinky=["{0}HandPinky{1}".format(side, i) for i in range(1, 4)],
        )

        self.right_leg = HumanLeg(upleg="{0}UpLeg".format(side),
                                  leg="{0}Leg".format(side),
                                  foot="{0}Foot".format(side),
                                  toe="{0}ToeBase".format(side))


class RigifySkeleton(HumanSkeleton):
    def __init__(self):
        self.spine = HumanSpine(
            head='DEF-spine.006',
            neck='DEF-spine.004',
            spine2='DEF-spine.003',
            spine1='DEF-spine.002',
            spine='DEF-spine.001',
            hips='DEF-spine'
        )

        side = 'L'
        self.left_arm = HumanArm(shoulder="DEF-shoulder.{0}".format(side),
                                 arm="DEF-upper_arm.{0}".format(side),
                                 forearm="DEF-forearm.{0}".format(side),
                                 hand="DEF-hand.{0}".format(side))

        self.left_fingers = HumanFingers(
            thumb=["DEF-thumb.{1:02d}.{0}".format(side, i) for i in range(1, 4)],
            index=["DEF-f_index.{1:02d}.{0}".format(side, i) for i in range(1, 4)],
            middle=["DEF-f_middle.{1:02d}.{0}".format(side, i) for i in range(1, 4)],
            ring=["DEF-f_ring.{1:02d}.{0}".format(side, i) for i in range(1, 4)],
            pinky=["DEF-f_pinky.{1:02d}.{0}".format(side, i) for i in range(1, 4)],
        )

        self.left_leg = HumanLeg(upleg="DEF-thigh.{0}".format(side),
                                 leg="DEF-shin.{0}".format(side),
                                 foot="DEF-foot.{0}".format(side),
                                 toe="DEF-toe.{0}".format(side))

        side = 'R'
        self.right_arm = HumanArm(shoulder="DEF-shoulder.{0}".format(side),
                                  arm="DEF-upper_arm.{0}".format(side),
                                  forearm="DEF-forearm.{0}".format(side),
                                  hand="DEF-hand.{0}".format(side))

        self.right_fingers = HumanFingers(
            thumb=["DEF-thumb.{1:02d}.{0}".format(side, i) for i in range(1, 4)],
            index=["DEF-f_index.{1:02d}.{0}".format(side, i) for i in range(1, 4)],
            middle=["DEF-f_middle.{1:02d}.{0}".format(side, i) for i in range(1, 4)],
            ring=["DEF-f_ring.{1:02d}.{0}".format(side, i) for i in range(1, 4)],
            pinky=["DEF-f_pinky.{1:02d}.{0}".format(side, i) for i in range(1, 4)],
        )

        self.right_leg = HumanLeg(upleg="DEF-thigh.{0}".format(side),
                                  leg="DEF-shin.{0}".format(side),
                                  foot="DEF-foot.{0}".format(side),
                                  toe="DEF-toe.{0}".format(side))


class RigifyMeta(HumanSkeleton):
    def __init__(self):
        self.spine = HumanSpine(
            head='spine.006',
            neck='spine.004',
            spine2='spine.003',
            spine1='spine.002',
            spine='spine.001',
            hips='spine'
        )

        side = 'L'
        self.left_arm = HumanArm(shoulder="shoulder.{0}".format(side),
                                 arm="upper_arm.{0}".format(side),
                                 forearm="forearm.{0}".format(side),
                                 hand="hand.{0}".format(side))

        self.left_fingers = HumanFingers(
            thumb=["thumb.{1:02d}.{0}".format(side, i) for i in range(1, 4)],
            index=["f_index.{1:02d}.{0}".format(side, i) for i in range(1, 4)],
            middle=["f_middle.{1:02d}.{0}".format(side, i) for i in range(1, 4)],
            ring=["f_ring.{1:02d}.{0}".format(side, i) for i in range(1, 4)],
            pinky=["f_pinky.{1:02d}.{0}".format(side, i) for i in range(1, 4)],
        )

        self.left_leg = HumanLeg(upleg="thigh.{0}".format(side),
                                 leg="shin.{0}".format(side),
                                 foot="foot.{0}".format(side),
                                 toe="toe.{0}".format(side))

        side = 'R'
        self.right_arm = HumanArm(shoulder="shoulder.{0}".format(side),
                                  arm="upper_arm.{0}".format(side),
                                  forearm="forearm.{0}".format(side),
                                  hand="hand.{0}".format(side))

        self.right_fingers = HumanFingers(
            thumb=["thumb.{1:02d}.{0}".format(side, i) for i in range(1, 4)],
            index=["f_index.{1:02d}.{0}".format(side, i) for i in range(1, 4)],
            middle=["f_middle.{1:02d}.{0}".format(side, i) for i in range(1, 4)],
            ring=["f_ring.{1:02d}.{0}".format(side, i) for i in range(1, 4)],
            pinky=["f_pinky.{1:02d}.{0}".format(side, i) for i in range(1, 4)],
        )

        self.right_leg = HumanLeg(upleg="thigh.{0}".format(side),
                                  leg="shin.{0}".format(side),
                                  foot="foot.{0}".format(side),
                                  toe="toe.{0}".format(side))


class UnrealSkeleton(HumanSkeleton):
    def __init__(self):
        self.spine = HumanSpine(
            head='head',
            neck='neck_01',
            spine2='spine_03',
            spine1='spine_02',
            spine='spine_01',
            hips='pelvis'
        )

        side = '_l'
        self.left_arm = HumanArm(shoulder="clavicle" + side,
                                 arm="upperarm" + side,
                                 forearm="lowerarm" + side,
                                 hand="hand" + side)

        self.left_fingers = HumanFingers(
                    thumb=["thumb_{0:02d}{1}".format(i, side) for i in range(1, 4)],
                    index=["index_{0:02d}{1}".format(i, side) for i in range(1, 4)],
                    middle=["middle_{0:02d}{1}".format(i, side) for i in range(1, 4)],
                    ring=["ring{0:02d}{1}".format(i, side) for i in range(1, 4)],
                    pinky=["pinky{0:02d}{1}".format(i, side) for i in range(1, 4)],
                )

        self.left_leg = HumanLeg(upleg="thigh{0}".format(side),
                                  leg="calf{0}".format(side),
                                  foot="foot{0}".format(side),
                                  toe="ball{0}".format(side))

        side = '_r'
        self.right_arm = HumanArm(shoulder="clavicle" + side,
                                 arm="upperarm" + side,
                                 forearm="lowerarm" + side,
                                 hand="hand" + side)

        self.right_fingers = HumanFingers(
                    thumb=["thumb_{0:02d}{1}".format(i, side) for i in range(1, 4)],
                    index=["index_{0:02d}{1}".format(i, side) for i in range(1, 4)],
                    middle=["middle_{0:02d}{1}".format(i, side) for i in range(1, 4)],
                    ring=["ring{0:02d}{1}".format(i, side) for i in range(1, 4)],
                    pinky=["pinky{0:02d}{1}".format(i, side) for i in range(1, 4)],
                )

        self.right_leg = HumanLeg(upleg="thigh{0}".format(side),
                                  leg="calf{0}".format(side),
                                  foot="foot{0}".format(side),
                                  toe="ball{0}".format(side))


# test
if __name__ == "__main__":
    rigify = RigifySkeleton()
    bone_map = rigify.conversion_map(MixamoSkeleton())

    print("Bone Map:")
    for k, v in bone_map.items():
        print('\t', k, v)
