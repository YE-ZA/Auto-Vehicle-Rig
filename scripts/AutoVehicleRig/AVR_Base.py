import maya.cmds as cmds
import maya.OpenMaya as om
import os
import re


def rename_group_model_world(vehicle_part_name):
    mesh = cmds.ls(sl=1)

    if not mesh:
        om.MGlobal.displayWarning('Please select at least one object!')
        return

    if vehicle_part_name in mesh:
        om.MGlobal.displayWarning("Please rename '{}' to avoid conflict".format(vehicle_part_name))
        return

    rule = re.compile(r'^[a-zA-Z_].*$')

    if not rule.match(vehicle_part_name):
        om.MGlobal.displayWarning("Please enter a valid name starting with 'a-z', 'A-Z', or'_'")
        return

    cmds.group(mesh, n=vehicle_part_name)

    for item in mesh:
        cmds.delete(item, ch=1)
        cmds.makeIdentity(item, a=1, n=0, pn=1)

    trans = cmds.ls(et='transform')

    for emptyGrp in trans:
        if not cmds.listRelatives(emptyGrp, c=1):
            cmds.delete(emptyGrp)

    cmds.move(0, 0, 0, '{}.rotatePivot'.format(vehicle_part_name), '{}.scalePivot'.format(vehicle_part_name), rpr=True)
    cmds.makeIdentity(vehicle_part_name, a=1, n=0, pn=1)


def rename_group_model_object(vehicle_part_name):
    mesh = cmds.ls(sl=1)

    if not mesh:
        om.MGlobal.displayWarning('Please select at least one object!')
        return

    if vehicle_part_name in mesh:
        om.MGlobal.displayWarning("Please rename '{}' to avoid conflict".format(vehicle_part_name))
        return

    rule = re.compile(r'^[a-zA-Z_].*$')

    if not rule.match(vehicle_part_name):
        om.MGlobal.displayWarning("Please enter a valid name starting with 'a-z', 'A-Z', or'_'")
        return

    cmds.group(mesh, n=vehicle_part_name)

    for item in mesh:
        cmds.delete(item, ch=1)
        cmds.makeIdentity(item, a=1, n=0, pn=1)

    trans = cmds.ls(et='transform')

    for emptyGrp in trans:
        if not cmds.listRelatives(emptyGrp, c=1):
            cmds.delete(emptyGrp)

    cmds.makeIdentity(vehicle_part_name, a=1, n=0, pn=1)


def create_joints_2w(vb_name, wf_name, wb_name, prefix='', suffix='_Jnt'):
    cmds.select(clear=True)

    jnt_vb = cmds.joint(p=(0, 0, 0))
    cmds.rename(jnt_vb, '{}{}{}'.format(prefix, vb_name, suffix))
    cmds.select(clear=True)

    jnt_wf = cmds.joint(p=(150, 0, 0))
    cmds.rename(jnt_wf, '{}{}{}'.format(prefix, wf_name, suffix))
    cmds.select(clear=True)

    jnt_wb = cmds.joint(p=(-150, 0, 0))
    cmds.rename(jnt_wb, '{}{}{}'.format(prefix, wb_name, suffix))
    cmds.select(clear=True)

    joint = ['{}{}{}'.format(prefix, vb_name, suffix),
             '{}{}{}'.format(prefix, wf_name, suffix),
             '{}{}{}'.format(prefix, wb_name, suffix)]

    for jnt in joint:
        cmds.joint(jnt, e=1, orientJoint='none', zeroScaleOrient=True)
        cmds.rotate(-90, 0, 0, jnt, forceOrderXYZ=True, relative=True, objectSpace=True)
        cmds.makeIdentity(jnt, apply=True, t=True, r=True, s=True, n=True, pn=True)

    for jnt in joint[1:]:
        cmds.parent(jnt, '{}{}{}'.format(prefix, vb_name, suffix))

    cmds.select(clear=True)


def create_joints_4w(vb_name, wfl_name, wfr_name, wbl_name, wbr_name, prefix='', suffix='_Jnt'):
    cmds.select(clear=True)

    jnt_vb = cmds.joint(p=(0, 0, 0))
    cmds.rename(jnt_vb, '{}{}{}'.format(prefix, vb_name, suffix))
    cmds.select(clear=True)

    jnt_wfl = cmds.joint(p=(150, 0, -150))
    cmds.rename(jnt_wfl, '{}{}{}'.format(prefix, wfl_name, suffix))
    cmds.select(clear=True)

    jnt_wfr = cmds.joint(p=(150, 0, 150))
    cmds.rename(jnt_wfr, '{}{}{}'.format(prefix, wfr_name, suffix))
    cmds.select(clear=True)

    jnt_wbl = cmds.joint(p=(-150, 0, -150))
    cmds.rename(jnt_wbl, '{}{}{}'.format(prefix, wbl_name, suffix))
    cmds.select(clear=True)

    jnt_wbr = cmds.joint(p=(-150, 0, 150))
    cmds.rename(jnt_wbr, '{}{}{}'.format(prefix, wbr_name, suffix))
    cmds.select(clear=True)

    joint = ['{}{}{}'.format(prefix, vb_name, suffix),
             '{}{}{}'.format(prefix, wfl_name, suffix),
             '{}{}{}'.format(prefix, wfr_name, suffix),
             '{}{}{}'.format(prefix, wbl_name, suffix),
             '{}{}{}'.format(prefix, wbr_name, suffix)]

    for jnt in joint:
        cmds.joint(jnt, e=1, orientJoint='none', zeroScaleOrient=True)
        cmds.rotate(-90, 0, 0, jnt, forceOrderXYZ=True, relative=True, objectSpace=True)
        cmds.makeIdentity(jnt, apply=True, t=True, r=True, s=True, n=True, pn=True)

    for jnt in joint[1:]:
        cmds.parent(jnt, '{}{}{}'.format(prefix, vb_name, suffix))

    cmds.select(clear=True)


def create_joints_6w(vb_name, wfl_name, wfr_name, wml_name, wmr_name, wbl_name, wbr_name, prefix='', suffix='_Jnt'):
    cmds.select(clear=True)

    jnt_vb = cmds.joint(p=(0, 0, 0))
    cmds.rename(jnt_vb, '{}{}{}'.format(prefix, vb_name, suffix))
    cmds.select(clear=True)

    jnt_wfl = cmds.joint(p=(150, 0, -150))
    cmds.rename(jnt_wfl, '{}{}{}'.format(prefix, wfl_name, suffix))
    cmds.select(clear=True)

    jnt_wfr = cmds.joint(p=(150, 0, 150))
    cmds.rename(jnt_wfr, '{}{}{}'.format(prefix, wfr_name, suffix))
    cmds.select(clear=True)

    jnt_wml = cmds.joint(p=(-150, 0, -150))
    cmds.rename(jnt_wml, '{}{}{}'.format(prefix, wml_name, suffix))
    cmds.select(clear=True)

    jnt_wmr = cmds.joint(p=(-150, 0, 150))
    cmds.rename(jnt_wmr, '{}{}{}'.format(prefix, wmr_name, suffix))
    cmds.select(clear=True)

    jnt_wbl = cmds.joint(p=(-300, 0, -150))
    cmds.rename(jnt_wbl, '{}{}{}'.format(prefix, wbl_name, suffix))
    cmds.select(clear=True)

    jnt_wbr = cmds.joint(p=(-300, 0, 150))
    cmds.rename(jnt_wbr, '{}{}{}'.format(prefix, wbr_name, suffix))
    cmds.select(clear=True)

    joint = ['{}{}{}'.format(prefix, vb_name, suffix),
             '{}{}{}'.format(prefix, wfl_name, suffix),
             '{}{}{}'.format(prefix, wfr_name, suffix),
             '{}{}{}'.format(prefix, wml_name, suffix),
             '{}{}{}'.format(prefix, wmr_name, suffix),
             '{}{}{}'.format(prefix, wbl_name, suffix),
             '{}{}{}'.format(prefix, wbr_name, suffix)]

    for jnt in joint:
        cmds.joint(jnt, e=1, orientJoint='none', zeroScaleOrient=True)
        cmds.rotate(-90, 0, 0, jnt, forceOrderXYZ=True, relative=True, objectSpace=True)
        cmds.makeIdentity(jnt, apply=True, t=True, r=True, s=True, n=True, pn=True)

    for jnt in joint[1:]:
        cmds.parent(jnt, '{}{}{}'.format(prefix, vb_name, suffix))

    cmds.select(clear=True)


def snap_joint():
    sel = cmds.ls(sl=1)

    if len(sel) < 2:
        om.MGlobal.displayWarning('Please select at least two objects!')
        return

    base_pos = cmds.xform(sel[-1], q=1, ws=1, piv=1)
    for item in sel[:-1]:
        cmds.move(base_pos[0], base_pos[1], base_pos[2], item)


def bind_skin_2w(vb_name, wf_name, wb_name, prefix='', suffix='_Jnt'):
    group = [vb_name, wf_name, wb_name]

    for grp in group:
        mesh = cmds.ls(grp, dag=1, et='mesh')  # Select all meshes within the group
        for obj in mesh:
            cmds.skinCluster(prefix + grp + suffix, obj, tsb=1)

    cmds.select(prefix + vb_name + suffix)


def bind_skin_4w(vb_name, wfl_name, wfr_name, wbl_name, wbr_name, prefix='', suffix='_Jnt'):
    group = [vb_name, wfl_name, wfr_name, wbl_name, wbr_name]

    for grp in group:
        mesh = cmds.ls(grp, dag=1, et='mesh')  # Select all meshes within the group
        for obj in mesh:
            cmds.skinCluster(prefix + grp + suffix, obj, tsb=1)

    cmds.select(prefix + vb_name + suffix)


def bind_skin_6w(vb_name, wfl_name, wfr_name, wml_name, wmr_name, wbl_name, wbr_name, prefix='', suffix='_Jnt'):
    group = [vb_name, wfl_name, wfr_name, wml_name, wmr_name, wbl_name, wbr_name]

    for grp in group:
        mesh = cmds.ls(grp, dag=1, et='mesh')  # Select all meshes within the group
        for obj in mesh:
            cmds.skinCluster(prefix + grp + suffix, obj, tsb=1)

    cmds.select(prefix + vb_name + suffix)


def create_controllers_2w(vb_name, wf_name, wb_name, prefix='', suffix='_Jnt'):
    USERSCRIPTDIR = cmds.internalVar(userScriptDir=True)
    PATH = os.path.join(USERSCRIPTDIR, 'AutoVehicleRig')
    cmds.file(PATH + '/BodyController.fbx', i=True, usingNamespaces=False)
    cmds.file(PATH + '/WheelController_2w.fbx', i=True, usingNamespaces=False)

    cmds.setAttr('VehicleBody_Ctrl.overrideEnabled', 1)
    cmds.setAttr('VehicleBody_Ctrl.overrideColor', 9)  # Purple
    base_pos = cmds.xform(prefix + vb_name + suffix, q=1, ws=1, piv=1)
    MinY = cmds.getAttr(wf_name + '.boundingBoxMinY')
    cmds.move(base_pos[0], MinY, base_pos[2], 'VehicleBody_Ctrl')

    wheel_pos = ['F', 'B']
    wheel_name = [wf_name, wb_name]
    for pos, item in zip(wheel_pos, wheel_name):
        cmds.setAttr('Wheel_{}_Ctrl.overrideEnabled'.format(pos), 1)
        cmds.setAttr('Wheel_{}_Ctrl.overrideColor'.format(pos), 17)  # Yellow

        base_pos = cmds.xform(item, q=1, ws=1, piv=1)
        cmds.move(base_pos[0], base_pos[1], base_pos[2], 'Wheel_{}_Ctrl'.format(pos))

    # Set up the constraints
    cmds.pointConstraint('VehicleBody_Ctrl', prefix + vb_name + suffix, maintainOffset=True)
    cmds.orientConstraint('VehicleBody_Ctrl', prefix + vb_name + suffix, maintainOffset=True)
    cmds.pointConstraint('Wheel_F_Ctrl', prefix + wf_name + suffix, maintainOffset=True)
    cmds.orientConstraint('Wheel_F_Ctrl', prefix + wf_name + suffix, maintainOffset=True)
    cmds.pointConstraint('Wheel_B_Ctrl', prefix + wb_name + suffix, maintainOffset=True)
    cmds.orientConstraint('Wheel_B_Ctrl', prefix + wb_name + suffix, maintainOffset=True)

    cmds.parent('Wheel_F_Ctrl', 'Wheel_B_Ctrl', 'VehicleBody_Ctrl')

    cmds.rename('VehicleBody_Ctrl', vb_name + '_Ctrl')
    cmds.rename('Wheel_F_Ctrl', wf_name + '_Ctrl')
    cmds.rename('Wheel_B_Ctrl', wb_name + '_Ctrl')

    cmds.select(clear=True)


def create_controllers_4w(vb_name, wfl_name, wfr_name, wbl_name, wbr_name, prefix='', suffix='_Jnt'):
    # Import controller files
    USERSCRIPTDIR = cmds.internalVar(userScriptDir=True)
    PATH = os.path.join(USERSCRIPTDIR, 'AutoVehicleRig')
    cmds.file(PATH + '/BodyController.fbx', i=True, usingNamespaces=False)
    cmds.file(PATH + '/WheelController_4w.fbx', i=True, usingNamespaces=False)

    # Set controller colors
    cmds.setAttr('VehicleBody_Ctrl.overrideEnabled', 1)
    cmds.setAttr('VehicleBody_Ctrl.overrideColor', 9)  # Purple
    base_pos = cmds.xform(prefix + vb_name + suffix, q=1, ws=1, piv=1)
    MaxY = cmds.getAttr(vb_name + '.boundingBoxMaxY')
    cmds.move(base_pos[0], MaxY+20, base_pos[2], 'VehicleBody_Ctrl')

    wheel_pos = ['FL', 'FR', 'BL', 'BR']
    wheel_name = [wfl_name, wfr_name, wbl_name, wbr_name]
    for pos, item in zip(wheel_pos, wheel_name):
        cmds.setAttr('Wheel_{}_Ctrl.overrideEnabled'.format(pos), 1)
        cmds.setAttr('Wheel_{}_Ctrl.overrideColor'.format(pos), 17)  # Yellow

        base_pos = cmds.xform(item, q=1, ws=1, piv=1)
        if pos == 'FL' or pos == 'BL':
            cmds.move(base_pos[0], base_pos[1], base_pos[2]-30, 'Wheel_{}_Ctrl'.format(pos))
        else:
            cmds.move(base_pos[0], base_pos[1], base_pos[2]+30, 'Wheel_{}_Ctrl'.format(pos))

    # Set up the constraints
    cmds.pointConstraint('VehicleBody_Ctrl', prefix + vb_name + suffix, maintainOffset=True)
    cmds.orientConstraint('VehicleBody_Ctrl', prefix + vb_name + suffix, maintainOffset=True)
    cmds.pointConstraint('Wheel_FL_Ctrl', prefix + wfl_name + suffix, maintainOffset=True)
    cmds.orientConstraint('Wheel_FL_Ctrl', prefix + wfl_name + suffix, maintainOffset=True)
    cmds.pointConstraint('Wheel_FR_Ctrl', prefix + wfr_name + suffix, maintainOffset=True)
    cmds.orientConstraint('Wheel_FR_Ctrl', prefix + wfr_name + suffix, maintainOffset=True)
    cmds.pointConstraint('Wheel_BL_Ctrl', prefix + wbl_name + suffix, maintainOffset=True)
    cmds.orientConstraint('Wheel_BL_Ctrl', prefix + wbl_name + suffix, maintainOffset=True)
    cmds.pointConstraint('Wheel_BR_Ctrl', prefix + wbr_name + suffix, maintainOffset=True)
    cmds.orientConstraint('Wheel_BR_Ctrl', prefix + wbr_name + suffix, maintainOffset=True)

    cmds.parent('Wheel_FL_Ctrl', 'Wheel_FR_Ctrl', 'Wheel_BL_Ctrl', 'Wheel_BR_Ctrl', 'VehicleBody_Ctrl')

    cmds.rename('VehicleBody_Ctrl', vb_name + '_Ctrl')
    cmds.rename('Wheel_FL_Ctrl', wfl_name + '_Ctrl')
    cmds.rename('Wheel_FR_Ctrl', wfr_name + '_Ctrl')
    cmds.rename('Wheel_BL_Ctrl', wbl_name + '_Ctrl')
    cmds.rename('Wheel_BR_Ctrl', wbr_name + '_Ctrl')

    cmds.select(clear=True)


def create_controllers_6w(vb_name, wfl_name, wfr_name, wml_name, wmr_name, wbl_name, wbr_name, prefix='', suffix='_Jnt'):
    USERSCRIPTDIR = cmds.internalVar(userScriptDir=True)
    PATH = os.path.join(USERSCRIPTDIR, 'AutoVehicleRig')
    cmds.file(PATH + '/BodyController.fbx', i=True, usingNamespaces=False)
    cmds.file(PATH + '/WheelController_6w.fbx', i=True, usingNamespaces=False)

    cmds.setAttr('VehicleBody_Ctrl.overrideEnabled', 1)
    cmds.setAttr('VehicleBody_Ctrl.overrideColor', 9)  # Purple
    base_pos = cmds.xform(prefix + vb_name + suffix, q=1, ws=1, piv=1)
    MaxY = cmds.getAttr(vb_name + '.boundingBoxMaxY')
    cmds.move(base_pos[0], MaxY + 20, base_pos[2], 'VehicleBody_Ctrl')

    wheel_pos = ['FL', 'FR', 'ML', 'MR', 'BL', 'BR']
    wheel_name = [wfl_name, wfr_name, wml_name, wmr_name, wbl_name, wbr_name]
    for pos, item in zip(wheel_pos, wheel_name):
        cmds.setAttr('Wheel_{}_Ctrl.overrideEnabled'.format(pos), 1)
        cmds.setAttr('Wheel_{}_Ctrl.overrideColor'.format(pos), 17)  # Yellow

        base_pos = cmds.xform(item, q=1, ws=1, piv=1)
        if pos == 'FL' or pos == 'ML' or pos == 'BL':
            cmds.move(base_pos[0], base_pos[1], base_pos[2] - 30, 'Wheel_{}_Ctrl'.format(pos))
        else:
            cmds.move(base_pos[0], base_pos[1], base_pos[2] + 30, 'Wheel_{}_Ctrl'.format(pos))

    # Set up the constraints
    cmds.pointConstraint('VehicleBody_Ctrl', prefix + vb_name + suffix, maintainOffset=True)
    cmds.orientConstraint('VehicleBody_Ctrl', prefix + vb_name + suffix, maintainOffset=True)
    cmds.pointConstraint('Wheel_FL_Ctrl', prefix + wfl_name + suffix, maintainOffset=True)
    cmds.orientConstraint('Wheel_FL_Ctrl', prefix + wfl_name + suffix, maintainOffset=True)
    cmds.pointConstraint('Wheel_FR_Ctrl', prefix + wfr_name + suffix, maintainOffset=True)
    cmds.orientConstraint('Wheel_FR_Ctrl', prefix + wfr_name + suffix, maintainOffset=True)
    cmds.pointConstraint('Wheel_ML_Ctrl', prefix + wml_name + suffix, maintainOffset=True)
    cmds.orientConstraint('Wheel_ML_Ctrl', prefix + wml_name + suffix, maintainOffset=True)
    cmds.pointConstraint('Wheel_MR_Ctrl', prefix + wmr_name + suffix, maintainOffset=True)
    cmds.orientConstraint('Wheel_MR_Ctrl', prefix + wmr_name + suffix, maintainOffset=True)
    cmds.pointConstraint('Wheel_BL_Ctrl', prefix + wbl_name + suffix, maintainOffset=True)
    cmds.orientConstraint('Wheel_BL_Ctrl', prefix + wbl_name + suffix, maintainOffset=True)
    cmds.pointConstraint('Wheel_BR_Ctrl', prefix + wbr_name + suffix, maintainOffset=True)
    cmds.orientConstraint('Wheel_BR_Ctrl', prefix + wbr_name + suffix, maintainOffset=True)

    cmds.parent('Wheel_FL_Ctrl', 'Wheel_FR_Ctrl', 'Wheel_ML_Ctrl', 'Wheel_MR_Ctrl', 'Wheel_BL_Ctrl', 'Wheel_BR_Ctrl', 'VehicleBody_Ctrl')

    cmds.rename('VehicleBody_Ctrl', vb_name + '_Ctrl')
    cmds.rename('Wheel_FL_Ctrl', wfl_name + '_Ctrl')
    cmds.rename('Wheel_FR_Ctrl', wfr_name + '_Ctrl')
    cmds.rename('Wheel_ML_Ctrl', wml_name + '_Ctrl')
    cmds.rename('Wheel_MR_Ctrl', wmr_name + '_Ctrl')
    cmds.rename('Wheel_BL_Ctrl', wbl_name + '_Ctrl')
    cmds.rename('Wheel_BR_Ctrl', wbr_name + '_Ctrl')

    cmds.select(clear=True)
