using System;

namespace NeuralNetwork
{
    internal class Program
    {
        static void Main(string[] args)
        {
            float[] inputs = { 0.1f, 0.3f, 0.4f, 0.6f, 0.8f, 0.9f };
            Neuron neuron = new Neuron(new float[] { 1f }, 0f);
            float learningRate = 0.1f;
            int numberOfEpochs = 500000;

            for (int epoch = 0; epoch < numberOfEpochs; epoch++)
            {
                foreach (float input in inputs)
                {
                    float target = input < 0.5f ? 0f : 1f;
                    neuron.Train(new float[] { input }, target, learningRate);
                }
            }

            Console.WriteLine("Testing neuron:");
            foreach (float input in inputs)
            {
                float output = neuron.Activate(new float[] { input });
                Console.WriteLine($"Input {input} -> Output {output:F4}");
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
            return 1 / (1 + MathF.Exp(-steepness * x));
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
