defmodule Sandbox do
  @moduledoc """
  Documentation for Sandbox.
  """

  @doc """
  Hello world.

  ## Examples

      iex> Sandbox.hello
      :world

  """
  def hello do
    :world
  end

  def list do
      [1, 2, 3]
  end

  def map do
      %{a: 1}
  end

  def listMap(list) do
      Enum.map(list, fn(item) ->
                item + 1
         end)
  end

  def listReduce(list) do
      Enum.reduce(list, 0, fn(item, acc) ->
                acc + item
         end)
  end

  def patternMatchReduce(list) do
      patternMatchReduce(list, 0)
  end


  defp patternMatchReduce([], acc) do
      acc
  end

  defp patternMatchReduce([h | t], acc) do
      patternMatchReduce(t, acc + h)
  end

  def piping(list) do
      list
      |> listMap
      |> listReduce
  end

  def destructure(%{a: aVal}) do
      aVal
  end

  def multiDespatch("hello") do
      "there"
  end

  def multiDespatch(other) do
      other
  end

end


defmodule MyMod do

def square(x) do
	x * x
end

end

defmodule MyOtherMod do

def apply(f, y) do
	f.(y)
end

end
