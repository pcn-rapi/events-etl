from etl.indivisible import group_meeting as indivisible_groupmtg
from etl.indivisible import action as indivisible_action
from etl.indivisible import group as indivisible_group
import json


indiv_groups = indivisible_group.grab_data()
indiv_groupmtg = indivisible_groupmtg.grab_data()
indiv_action = indivisible_action.grab_data()

data = indiv_groupmtg + indiv_action + indiv_groups
print(json.dumps(data))
