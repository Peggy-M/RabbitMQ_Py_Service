# 跨语言可靠通讯：使用 MQ 实现 Java 与 Python 服务的可靠性交互

> 在之前的一个项目当中存在这样的一个需求，其主要是要完成 Java 与 Python 之间的非阻塞式的实时数据交互。
>
> 业务的场景是将真实环境下的试试物理数据采集之后，通过算法分析最终在客户端的网页实时的展示，而整个业务的核心有两侧个重点；
>
> 1.算法的预测模型是 Web 客户端下根据不同的业务场景与历史物理数据训练而成，也就是说模型的复用率比较低，这就要求针对不同的场景要实时的训练。
>
> 2.训练好的模型只针对与某一场景进行数据的采集实时预测，并且同时保证数据的可靠性与实时性，其主要是在 Web 客户端实时的以大数据的形式更新。

对于跨语言的交互，其实本身没有任何的瓶颈限制，因为本身即便是对于 Java 也是封装了很多由 C/C++ 实现的 native 方法，但较为棘手的点在于，如果保证语言之间低耦合以及可靠、高效的交互。

从低耦合的角度出发是因为，我想让 Java 的与 Python 从业务模块上分离开，Java 只负责对数据的过滤筛选,而 Python 只负责过程模型的训练以及算法的预测。同时对于 Python 的内部我想将与 Java 交互的部分与模型训练生成的部分也分离开，保证当算法模型预测与训练业务发生变动，而不影响 Python 与 Java 之间的数据通讯模块。

从可靠性与实时性的角度，其本身是属于 Java 与 Python 交互部分，如果采用传统的 HTTP/REST API 暴露接口的这种方式，虽然可以将 Java 与 Python 从代码层面解耦，但却这种传统的 HTTP 请求会因为网络波动,以及单向交互导致消息的实时性是很难保证的。但如果采用双向通讯的 Socket 连接正好是满足这种实时性的交互需求的。
