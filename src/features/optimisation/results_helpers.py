class SubIterationResult:
    evaluation_count = 0
    cost_fun_list = None

    def __init__(self):
        self.cost_fun_list = []
        self.evaluation_count = 0

    def add_sub_iteration_result(self, cost_function: float):
        self.evaluation_count += 1
        self.cost_fun_list.append(cost_function)

    def get_func_list(self):
        return self.cost_fun_list
