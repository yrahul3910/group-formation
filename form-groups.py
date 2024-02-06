from collections import Counter

from tabulate import tabulate
import pandas as pd


GROUP_SIZE = 3


def find_tuples(n, current_tuple=(), start=1):
    tuples = []
    if n == 0:
        return [current_tuple]

    for i in range(start, n + 1):
        if i <= n:
            new_tuple = find_tuples(n - i, current_tuple + (i,), i)
            if len(new_tuple) > 0:
                tuples.extend(new_tuple)

    return tuples


df = pd.read_excel("CSC591 Spring 2024 Project Groups (Responses).xlsx")

groups = []
partial_groups = []

for idx, row in df.iterrows():
    own_group_resp = row["Do you want to form your own group?"]
    if own_group_resp == f"Yes, and I have a group of {GROUP_SIZE}":
        members = row[
            "Please enter the NCSU email IDs of your group members, separated by commas."
        ].split(",")

        if len(members) == GROUP_SIZE - 1:
            members.append(row["What is your NCSU email ID?"])
        if len(members) < GROUP_SIZE - 1:
            print("Error in row", idx)

        groups.append(members)
    elif own_group_resp == "No":
        partial_groups.append([row["What is your NCSU email ID?"]])
    else:
        # Partial groups
        members = row[
            "Please enter the email IDs of your group members, separated by commas."
        ].split(",")

        #if len(members) != int(
        #    row["How many group members do you have (including yourself)?"]
        #):
        #    members.append(row["What is your NCSU email ID?"])

        partial_groups.append(members)


print("Initial statistics:")
print("=" * len("Initial statistics:"))
print("Number of complete groups:", len(groups))
print("Partial groups:")

# Map partial group sizes to number of partial groups of that size
partial_group_sizes = {
    size: len([x for x in partial_groups if len(x) == size])
    for size in range(1, GROUP_SIZE + 1)
}

for size in range(1, GROUP_SIZE):
    print(f"\tsize {size}:", partial_group_sizes[size])
print()

# Get a list of tuples that add up to GROUP_SIZE.
# We will use these tuples to merge partial groups together.
tuples = find_tuples(GROUP_SIZE)

# Merge partial groups together
for t in reversed(tuples):
    print('-----')
    print(t)

    # Need to update this each iteration
    partial_group_sizes = {
        size: len([x for x in partial_groups if len(x) == size])
        for size in range(1, GROUP_SIZE + 1)
    }
    print("partial_group_sizes =", partial_group_sizes)

    # Find partial groups whose size is in t
    # and merge them together to form a complete group
    groups_to_merge = {
        size: [pgroup for pgroup in partial_groups if len(pgroup) == size] for size in t
    }

    # We can only merge the minimum number
    cur_sizes = [partial_group_sizes[size] for size in t]
    print("cur_sizes =", cur_sizes)

    max_value_count = max(Counter(cur_sizes).values())
    print("max_value_count =", max_value_count)

    min_size = int(min(cur_sizes) // max_value_count)
    print("min_size =", min_size)

    for _ in range(min_size):
        new_group = []
        for size in t:
            groups_to_add = groups_to_merge[size].pop()
            new_group.extend(groups_to_add)

            # Now remove the partial group from the list
            partial_groups.remove(groups_to_add)

        groups.append(new_group)

print("After merging:")
print("=" * len("After merging:"))
print("Number of complete groups:", len(groups))
print("Partial groups:")

partial_group_sizes = {
    size: len([x for x in partial_groups if len(x) == size])
    for size in range(1, GROUP_SIZE)
}

for size in range(1, GROUP_SIZE):
    print(f"\tsize {size}:", partial_group_sizes[size])
print()

print(tabulate(groups))
print()
print(len(groups), "groups created.")

# Map email IDs to names
names_df = pd.read_csv("courseid_1771_participants.csv")
for i in range(len(groups)):
    for j in range(len(groups[i])):
        name_row = names_df[names_df["Email address"] == groups[i][j].lower().strip()]
        name_row = name_row.values.tolist()

        if len(name_row) > 0:
            groups[i][j] = name_row[0][2] + ", " + name_row[0][0]

out_df = pd.DataFrame(groups, columns=[f"Member {i}" for i in range(1, GROUP_SIZE + 1)])
out_df.to_csv("out.csv")
print("Written to out.csv")

if len(partial_groups) > 0:
    print("WARN: There are still partial groups left.")
    print("WARN: These partial groups are:")
    print(tabulate(partial_groups))
