from cass import predict

sum = 0
right = 0
with open('pos.txt', 'r') as f:
    line = f.readline()
    while line:
        sum = sum + 1
        line = f.readline()
        ans = predict.predict_one(line)
        if ans == 1:
            right = right + 1

        print(sum)
        print(right / sum)
        print("")

with open('neg.txt', 'r') as f:
    line = f.readline()
    while line:
        sum = sum + 1
        line = f.readline()
        ans = predict.predict_one(line)
        if ans == 0:
            right = right + 1

        print(sum)
        print(right / sum)
        print("")

print("ans")
print(right / sum)
