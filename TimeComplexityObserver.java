import java.util.Random;

public class TimeComplexityObserver {

    public static void insertionSort(int[] arr) {
        int n = arr.length;
        for (int i = 1; i < n; ++i) {
            int key = arr[i];
            int j = i - 1;

            while (j >= 0 && arr[j] > key) {
                arr[j + 1] = arr[j];
                j = j - 1;
            }
            arr[j + 1] = key;
        }
    }

    public static void bubbleSort(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }
    }

    public static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pi = partition(arr, low, high);
            quickSort(arr, low, pi - 1);
            quickSort(arr, pi + 1, high);
        }
    }

    private static int partition(int[] arr, int low, int high) {
        int pivot = arr[high];
        int i = (low - 1); 
        for (int j = low; j < high; j++) {
            if (arr[j] <= pivot) {
                i++;

                int temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }

        int temp = arr[i + 1];
        arr[i + 1] = arr[high];
        arr[high] = temp;

        return i + 1;
    }

    public static int[] generateRandomArray(int size) {
        int[] arr = new int[size];
        Random rand = new Random();
        for (int i = 0; i < size; i++) {
            arr[i] = rand.nextInt(size * 10); 
        }
        return arr;
    }

    public static void main(String[] args) {
        int[] inputSizes = {100, 1000, 5000, 10000, 20000, 50000}; 

        System.out.println("Empirical Observation of Time Complexity\n");
        System.out.printf("%10s | %15s | %15s | %15s\n", "Input Size", "Insertion Sort (ms)", "Bubble Sort (ms)", "Quick Sort (ms)");
        System.out.println("-------------------------------------------------------------------");

        for (int size : inputSizes) {
            int[] originalArray = generateRandomArray(size);

            int[] arrInsertion = originalArray.clone();
            long startTimeInsertion = System.currentTimeMillis();
            insertionSort(arrInsertion);
            long endTimeInsertion = System.currentTimeMillis();
            long durationInsertion = endTimeInsertion - startTimeInsertion;

            int[] arrBubble = originalArray.clone();
            long startTimeBubble = System.currentTimeMillis();
            bubbleSort(arrBubble);
            long endTimeBubble = System.currentTimeMillis();
            long durationBubble = endTimeBubble - startTimeBubble;

            int[] arrQuick = originalArray.clone();
            long startTimeQuick = System.currentTimeMillis();
            quickSort(arrQuick, 0, arrQuick.length - 1);
            long endTimeQuick = System.currentTimeMillis();
            long durationQuick = endTimeQuick - startTimeQuick;

            System.out.printf("%10d | %15d | %15d | %15d\n", size, durationInsertion, durationBubble, durationQuick);
        }
    }
}
