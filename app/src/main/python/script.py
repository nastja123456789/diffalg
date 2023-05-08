# import numpy as np
# from scipy.stats import multivariate_normal
# def gmm_alg(M):
#     x = np.zeros((len(M), 2))
#     for i, a in enumerate(M):
#         x[i] = [i, a**2]
#     # gm = GMM(k=2)
#     np.random.seed(70)
#     gm = GMM(3)
#     # gm = GMM(n_components=2)
#     gm.fit(x)
#     clusters = gm.predict(x)
#     cl = []
#     # for i, j in enumerate(clusters):
#     #     print(i)
#     #     if j == 'comp0':
#     #         cl.append(0)
#     #     elif j == 'comp1':
#     #         cl.append(1)
#     first = []
#     zeros = []
#     for i, j in enumerate(clusters):
#         if j == 1:
#             first.insert(0, M[i])
#         else:
#             zeros.insert(0, M[i])
#     watermark = ""
#     def mode(ls):
#         counts = {}
#         for item in ls:
#             if item in counts:
#                 counts[item] += 1
#             else:
#                 counts[item] = 1
#         return [key for key in counts.keys() if counts[key] == max(counts.values())]
#
#     mode_zeros = mode(zeros)
#     mode_first = mode(first)
#     if mode(mode_zeros) > mode(mode_first):
#         for j in clusters:
#             if j == 0:
#                 watermark += "1"
#             else:
#                 watermark += "0"
#     else:
#         for j in clusters:
#             if j == 0:
#                 watermark += "0"
#             else:
#                 watermark += "1"
#     return watermark
#
# class GMM:
#     def __init__(self, k, max_iter=5):
#         self.k = k
#         self.max_iter = int(max_iter)
#
#     def initialize(self, X):
#         self.shape = X.shape
#         self.n, self.m = self.shape
#
#         self.phi = np.full(shape=self.k, fill_value=1/self.k)
#         self.weights = np.full( shape=self.shape, fill_value=1/self.k)
#
#         random_row = np.random.randint(low=0, high=self.n, size=self.k)
#         self.mu = [  X[row_index,:] for row_index in random_row ]
#         self.sigma = [ np.cov(X.T) for _ in range(self.k) ]
#
#     def e_step(self, X):
#         # E-Step: update weights and phi holding mu and sigma constant
#         self.weights = self.predict_proba(X)
#         self.phi = self.weights.mean(axis=0)
#
#     def m_step(self, X):
#         # M-Step: update mu and sigma holding phi and weights constant
#         for i in range(self.k):
#             weight = self.weights[:, [i]]
#             total_weight = weight.sum()
#             self.mu[i] = (X * weight).sum(axis=0) / total_weight
#             self.sigma[i] = np.cov(X.T,
#                                    aweights=(weight/total_weight).flatten(),
#                                    bias=True)
#
#     def fit(self, X):
#         self.initialize(X)
#
#         for iteration in range(self.max_iter):
#             self.e_step(X)
#             self.m_step(X)
#
#     def predict_proba(self, X):
#         likelihood = np.zeros( (self.n, self.k) )
#         for i in range(self.k):
#             distribution = multivariate_normal(
#                 mean=self.mu[i],
#                 cov=self.sigma[i])
#             likelihood[:,i] = distribution.pdf(X)
#
#         numerator = likelihood * self.phi
#         denominator = numerator.sum(axis=1)[:, np.newaxis]
#         weights = numerator / denominator
#         return weights
#
#     def predict(self, X):
#         weights = self.predict_proba(X)
#         return np.argmax(weights, axis=1)
#
# # class GMM:
# #     def __init__(self, n_components, max_iter=100, comp_names=None):
# #         self.n_components = n_components
# #         self.max_iter = max_iter
# #         if comp_names is None:
# #             self.comp_names = [f"comp{index}" for index in range(self.n_components)]
# #         else:
# #             self.comp_names = comp_names
# #         self.pi = [1 / self.n_components for _ in range(self.n_components)]
# #
# #     def multivariate_normal(self, X, mean_vector, covariance_matrix):
# #         return (2 * np.pi) ** (-len(X) / 2) * np.linalg.det(covariance_matrix) ** (-1 / 2) * np.exp(
# #             -np.dot(np.dot((X - mean_vector).T, np.linalg.inv(covariance_matrix)), (X - mean_vector)) / 2)
# #
# #     def fit(self, X):
# #         new_X = np.array_split(X, self.n_components)
# #         self.mean_vector = [np.mean(x, axis=0) for x in new_X]
# #         self.covariance_matrixes = [np.cov(x.T) for x in new_X]
# #         del new_X
# #         for iteration in range(self.max_iter):
# #             self.r = np.zeros((len(X), self.n_components))
# #             for n in range(len(X)):
# #                 for k in range(self.n_components):
# #                     self.r[n][k] = self.pi[k] * self.multivariate_normal(X[n], self.mean_vector[k], self.covariance_matrixes[k])
# #                     self.r[n][k] /= sum([self.pi[j] * self.multivariate_normal(X[n], self.mean_vector[j], self.covariance_matrixes[j]) for j in range(self.n_components)])
# #             N = np.sum(self.r, axis=0)
# #             self.mean_vector = np.zeros((self.n_components, len(X[0])))
# #             for k in range(self.n_components):
# #                 for n in range(len(X)):
# #                     self.mean_vector[k] += self.r[n][k] * X[n]
# #                 self.mean_vector[k] = 1 / N[k] * self.mean_vector[k]
# #             self.covariance_matrixes = [np.zeros((len(X[0]), len(X[0]))) for k in range(self.n_components)]
# #             for k in range(self.n_components):
# #                 self.covariance_matrixes[k] = np.cov(X.T, aweights=(self.r[:, k]), ddof=0)
# #                 self.covariance_matrixes[k] = 1 / N[k] * self.covariance_matrixes[k]
# #             self.pi = [N[k] / len(X) for k in range(self.n_components)]
# #
# #     def predict(self, X):
# #         probas = []
# #         for n in range(len(X)):
# #             probas.append([self.multivariate_normal(X[n], self.mean_vector[k], self.covariance_matrixes[k])
# #                            for k in range(self.n_components)])
# #         cluster = []
# #         for proba in probas:
# #             cluster.append(self.comp_names[proba.index(max(proba))])
# #         return cluster
#
# # class GMM:
# #     def __init__(self, n_components, max_iter = 100, comp_names=None):
# #         self.n_componets = n_components
# #         self.max_iter = max_iter
# #         if comp_names == None:
# #             self.comp_names = [f"comp{index}" for index in range(self.n_componets)]
# #         else:
# #             self.comp_names = comp_names
# #         self.pi = [1/self.n_componets for comp in range(self.n_componets)]
# #     def multivariate_normal(self, X, mean_vector, covariance_matrix):
# #         return (2*np.pi)**(-len(X)/2)*np.linalg.det(covariance_matrix)**(-1/2)*np.exp(-np.dot(np.dot((X-mean_vector).T, np.linalg.inv(covariance_matrix)), (X-mean_vector))/2)
# #
# #     def fit(self, X):
# #         new_X = np.array_split(X, self.n_componets)
# #         self.mean_vector = [np.mean(x, axis=0) for x in new_X]
# #         self.covariance_matrixes = [np.cov(x.T) for x in new_X]
# #         del new_X
# #         for iteration in range(self.max_iter):
# #             self.r = np.zeros((len(X), self.n_componets))
# #             for n in range(len(X)):
# #                 for k in range(self.n_componets):
# #                     self.r[n][k] = self.pi[k] * self.multivariate_normal(X[n], self.mean_vector[k], self.covariance_matrixes[k])
# #                     self.r[n][k] /= sum([self.pi[j]*self.multivariate_normal(X[n], self.mean_vector[j], self.covariance_matrixes[j]) for j in range(self.n_componets)])
# #             N = np.sum(self.r, axis=0)
# #             self.mean_vector = np.zeros((self.n_componets, len(X[0])))
# #             for k in range(self.n_componets):
# #                 for n in range(len(X)):
# #                     self.mean_vector[k] += self.r[n][k] * X[n]
# #             self.mean_vector = [1/N[k]*self.mean_vector[k] for k in range(self.n_componets)]
# #             self.covariance_matrixes = [np.zeros((len(X[0]), len(X[0]))) for k in range(self.n_componets)]
# #             for k in range(self.n_componets):
# #                 self.covariance_matrixes[k] = np.cov(X.T, aweights=(self.r[:, k]), ddof=0)
# #             self.covariance_matrixes = [1/N[k]*self.covariance_matrixes[k] for k in range(self.n_componets)]
# #             self.pi = [N[k]/len(X) for k in range(self.n_componets)]
# #     def predict(self, X):
# #         probas = []
# #         for n in range(len(X)):
# #             probas.append([self.multivariate_normal(X[n], self.mean_vector[k], self.covariance_matrixes[k])
# #                            for k in range(self.n_componets)])
# #         cluster = []
# #         for proba in probas:
# #             cluster.append(self.comp_names[proba.index(max(proba))])
# #         return cluster
# # class GMM:
# #     def __init__(self, n_components, max_iter = 100, comp_names=None):
# #         self.n_componets = n_components
# #         self.max_iter = max_iter
# #         if comp_names == None:
# #             self.comp_names = [f"comp{index}" for index in range(self.n_componets)]
# #         else:
# #             self.comp_names = comp_names
# #         self.pi = [1/self.n_componets for comp in range(self.n_componets)]
# #     def fit(self, X):
# #         new_X = np.array_split(X, self.n_componets)
# #         self.mean_vector = [np.mean(x, axis=0) for x in new_X]
# #         self.covariance_matrixes = [np.cov(x.T) for x in new_X]
# #         del new_X
# #     def multivariate_normal(self, X, mean_vector, covariance_matrix):
# #         return (2*np.pi)**(-len(X)/2)*np.linalg.det(covariance_matrix)**(-1/2)*np.exp(-np.dot(np.dot((X-mean_vector).T, np.linalg.inv(covariance_matrix)), (X-mean_vector))/2)
# #     def predict(self, X):
# #         probas = []
# #         for n in range(len(X)):
# #             probas.append([self.multivariate_normal(X[n], self.mean_vector[k], self.covariance_matrixes[k])
# #                            for k in range(self.n_componets)])
# #         cluster = []
# #         for proba in probas:
# #             cluster.append(self.comp_names[proba.index(max(proba))])
# #         return cluster
#
# # def main(M):
# #     q = Queue()
# #     p = Process(target=gmm_alg, args=(M, q))
# #     p.start()
# #     p.join()
# #     watermark = q.get()
# #     return watermark
# # def main():
# #     return "010101010101010101010101"
# # import numpy as np
# # import statistics
# # from sklearn.mixture import GaussianMixture
# # from multiprocessing import Pool
# #
# # def gmm_alg(M):
# #     x = np.zeros((len(M), 2))
# #     for i, a in enumerate(M):
# #         x[i] = [i, a**2]
# #
# #     gm = GaussianMixture(n_components=2)
# #     gm.fit(x)
# #     clusters = gm.predict(x)
# #
# #     first = []
# #     zeros = []
# #
# #     def process_cluster(i):
# #         if clusters[i] == 1:
# #             first.insert(0, M[i])
# #         else:
# #             zeros.insert(0, M[i])
# #
# #     with Pool() as pool:
# #         pool.map(process_cluster, range(len(clusters)))
# #
# #     watermark = ""
# #     if statistics.mode(zeros) > statistics.mode(first):
# #         for j in clusters:
# #             if j == 0:
# #                 watermark += "1"
# #             else:
# #                 watermark += "0"
# #     else:
# #         for j in clusters:
# #             if j == 0:
# #                 watermark += "0"
# #             else:
# #                 watermark += "1"
# #
# #     return watermark
# #
# # import numpy as np
# # import statistics
# # from sklearn.mixture import GaussianMixture
# # from multiprocessing import Pool
# #
# # def gmm_alg(M):
# #     x = np.zeros((len(M), 2))
# #     for i, a in enumerate(M):
# #         x[i] = [i, a**2]
# #     gm = GaussianMixture(n_components=2)
# #     gm.fit(x)
# #     clusters = gm.predict(x)
# #     first = []
# #     zeros = []
# #     for i, j in enumerate(clusters):
# #         if j == 1:
# #             first.insert(0, M[i])
# #         else:
# #             zeros.insert(0, M[i])
# #
# #     watermark = ""
# #     mode_zeros = statistics.mode(zeros)
# #     mode_first = statistics.mode(first)
# #
# #     def process_cluster(j):
# #         if j == 0:
# #             watermark += "1"
# #         else:
# #             watermark += "0"
# #
# #     if mode_zeros > mode_first:
# #         with Pool() as pool:
# #             pool.map(process_cluster, clusters)
# #     else:
# #         with Pool() as pool:
# #             pool.map(process_cluster, clusters)
# #     return watermark
#
# # from multiprocessing import Process
# #
# # def f(name):
# #     pass
# #
# # p = Process(target=f, args=('bob',))
# # p.start()
# # p.join()

import numpy as np
from scipy.stats import multivariate_normal

def gmm_alg(M):
    x = np.zeros((len(M), 2))
    for i, a in enumerate(M):
        x[i] = [i, a**2]
    # np.random.seed(70)
    # gm = GMM(4)
    gm = GMM(2)
    gm.fit(x)
    clusters = gm.predict(x)
    first = []
    zeros = []
    for i, j in enumerate(clusters):
        if j == 1:
            first.insert(0, M[i])
        else:
            zeros.insert(0, M[i])
    watermark = ""
    def mode(ls):
        counts = {}
        for item in ls:
            if item in counts:
                counts[item] += 1
            else:
                counts[item] = 1
        return [key for key in counts.keys() if counts[key] == max(counts.values())]


    mode_zeros = mode(zeros)
    mode_first = mode(first)
    if mode(mode_zeros) > mode(mode_first):
        for j in clusters:
            if j == 0:
                watermark += "1"
            else:
                watermark += "0"
    else:
        for j in clusters:
            if j == 0:
                watermark += "0"
            else:
                watermark += "1"
    return watermark




class GMM:
    def __init__(self, k, max_iter=5):
        self.k = k
        self.max_iter = int(max_iter)

    def initialize(self, X):
        self.shape = X.shape
        self.n, self.m = self.shape

        self.phi = np.full(shape=self.k, fill_value=1/self.k)
        self.weights = np.full(shape=self.shape, fill_value=1/self.k)
        # random_row = [1,3,3,3,3]
        random_row = np.random.randint(low=0, high=self.n, size=self.k)
        self.mu = [  X[row_index,:] for row_index in random_row ]
        self.sigma = [ np.cov(X.T) for _ in range(self.k) ]

    def e_step(self, X):
        self.weights = self.predict_proba(X)
        self.phi = self.weights.mean(axis=0)

    def m_step(self, X):
        for i in range(self.k):
            weight = self.weights[:, [i]]
            total_weight = weight.sum()
            self.mu[i] = (X * weight).sum(axis=0) / total_weight
            self.sigma[i] = np.cov(X.T,
                                   aweights=(weight/total_weight).flatten(),
                                   bias=True)

    def fit(self, X):
        self.initialize(X)
        for iteration in range(self.max_iter):
            self.e_step(X)
            self.m_step(X)

    def predict_proba(self, X):
        likelihood = np.zeros( (self.n, self.k) )
        for i in range(self.k):
            distribution = multivariate_normal(
                mean=self.mu[i],
                cov=self.sigma[i])
            likelihood[:,i] = distribution.pdf(X)
        numerator = likelihood * self.phi
        denominator = numerator.sum(axis=1)[:, np.newaxis]
        weights = numerator / denominator
        return weights

    def predict(self, X):
        weights = self.predict_proba(X)
        return np.argmax(weights, axis=1)
