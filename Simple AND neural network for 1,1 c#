using System;

namespace NeuralNetwork
{
    internal class Program
    {
        static void Main(string[] args)
        {
            float[][] inputs = {
                new float[] { 0f, 0f },
                new float[] { 0f, 1f },
                new float[] { 1f, 0f },
                new float[] { 1f, 1f }
            };

            float[] targets = { 0f, 0f, 0f, 1f }; // AND logic

            Neuron neuron1 = new Neuron(new float[] { 1f }, 0f);
            Neuron neuron2 = new Neuron(new float[] { 1f }, 0f);
            Neuron outputNeuron = new Neuron(new float[] { 1f, 1f }, 0f);

            float learningRate = 0.1f;
            int epochs = 50000;

            for (int epoch = 0; epoch < epochs; epoch++)
            {
                for (int i = 0; i < inputs.Length; i++)
                {
                    float out1 = neuron1.Activate(new float[] { inputs[i][0] });
                    float out2 = neuron2.Activate(new float[] { inputs[i][1] });

                    outputNeuron.Train(new float[] { out1, out2 }, targets[i], learningRate);
                }
            }

            Console.WriteLine("Testing AND neuron:");
            for (int i = 0; i < inputs.Length; i++)
            {
                float out1 = neuron1.Activate(new float[] { inputs[i][0] });
                float out2 = neuron2.Activate(new float[] { inputs[i][1] });
                float result = outputNeuron.Activate(new float[] { out1, out2 });
                Console.WriteLine($"Input [{inputs[i][0]}, {inputs[i][1]}] -> Output {result:F4}");
            }
        }
    }

    public class Neuron
    {
        public float[] Weights;
        public float Bias;

        public Neuron(float[] weights, float bias)
        {
            Weights = weights;
            Bias = bias;
        }

        public float Activate(float[] inputs)
        {
            float sum = Bias;
            for (int i = 0; i < inputs.Length; i++)
                sum += inputs[i] * Weights[i];

            return Sigmoid(sum);
        }

        private float Sigmoid(float x)
        {
            float steepness = 10f;
            float z = steepness * x;
            if (z > 20f) z = 20f;
            if (z < -20f) z = -20f;
            return 1 / (1 + MathF.Exp(-z));
        }

        public void Train(float[] inputs, float target, float learningRate)
        {
            float output = Activate(inputs);
            float error = output - target;
            float delta = error * output * (1 - output);

            for (int i = 0; i < Weights.Length; i++)
                Weights[i] -= learningRate * delta * inputs[i];

            Bias -= learningRate * delta;
        }
    }
}
